"""
cdp.py — Мінімальний клієнт Chrome DevTools Protocol на чистій стандартній
бібліотеці Python 3 (без pip / сторонніх залежностей → $0 бюджет).

Реалізовано:
  * запуск headless Chrome у тимчасовому профілі;
  * мінімальний WebSocket-клієнт (RFC 6455, лише текстові кадри);
  * обгортка CDP-сесії: navigate / evaluate / metrics / print-media / console.

Авторська угода: кожна команда CDP повертає словник result.
"""

import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import tempfile
import time
import urllib.request
from urllib.parse import urlparse

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome():
    """Повертає шлях до браузера або None."""
    for path in CHROME_CANDIDATES:
        if os.path.isfile(path):
            return path
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    return None


class WebSocket(object):
    """Мінімальний WebSocket-клієнт (клієнт -> сервер, текстові кадри)."""

    def __init__(self, url, timeout=30):
        parts = urlparse(url)
        host = parts.hostname
        port = parts.port or 80
        path = parts.path + (("?" + parts.query) if parts.query else "")

        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        self.buffer = b""

        key = base64.b64encode(os.urandom(16)).decode("ascii")
        handshake = (
            "GET %s HTTP/1.1\r\n"
            "Host: %s:%d\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: %s\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n" % (path, host, port, key)
        )
        self.sock.sendall(handshake.encode("ascii"))

        header = self._read_until(b"\r\n\r\n")
        if b"101" not in header.split(b"\r\n")[0]:
            raise RuntimeError("WebSocket handshake failed: %r" % header[:200])

    def _read_until(self, marker):
        while marker not in self.buffer:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise RuntimeError("Connection closed during handshake")
            self.buffer += chunk
        index = self.buffer.index(marker) + len(marker)
        head, self.buffer = self.buffer[:index], self.buffer[index:]
        return head

    def _recv_exact(self, count):
        while len(self.buffer) < count:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise RuntimeError("Connection closed while reading frame")
            self.buffer += chunk
        data, self.buffer = self.buffer[:count], self.buffer[count:]
        return data

    def send(self, text):
        payload = text.encode("utf-8")
        header = bytearray([0x81])  # FIN + text frame
        length = len(payload)
        if length < 126:
            header.append(0x80 | length)
        elif length < (1 << 16):
            header.append(0x80 | 126)
            header += struct.pack(">H", length)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", length)
        mask = os.urandom(4)
        header += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(header) + masked)

    def recv(self):
        """Повертає текстове повідомлення або None під час таймауту."""
        b1, b2 = self._recv_exact(2)
        opcode = b1 & 0x0F
        length = b2 & 0x7F
        if length == 126:
            length = struct.unpack(">H", self._recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self._recv_exact(8))[0]
        payload = self._recv_exact(length) if length else b""
        if opcode == 0x8:
            raise RuntimeError("WebSocket closed by peer")
        if opcode in (0x9, 0xA):  # ping/pong
            return self.recv()
        return payload.decode("utf-8", "replace")

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


class Browser(object):
    """Керує headless Chrome через CDP."""

    def __init__(self, headless=True, timeout=30):
        self.chrome = find_chrome()
        if not self.chrome:
            raise RuntimeError("Chrome/Chromium не знайдено у системі")
        self.headless = headless
        self.timeout = timeout
        self.proc = None
        self.port = None
        self.profile = None
        self.ws = None
        self.msg_id = 0
        self.console = []
        self.page_errors = []
        self.failed_requests = []

    # ---------- життєвий цикл ----------
    def start(self):
        self.port = self._free_port()
        self.profile = tempfile.mkdtemp(prefix="chancery-chrome-")
        args = [
            self.chrome,
            "--remote-debugging-port=%d" % self.port,
            "--user-data-dir=%s" % self.profile,
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-sync",
            "--disable-dev-shm-usage",
            "--window-size=1280,1024",
            "about:blank",
        ]
        if self.headless:
            args.insert(1, "--headless=new")
        self.proc = subprocess.Popen(
            args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        target = self._wait_for_target()
        self.ws = WebSocket(target, timeout=self.timeout)
        self.send("Page.enable")
        self.send("Runtime.enable")
        self.send("Log.enable")
        self.send("Network.enable")
        return self

    def _free_port(self):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]

    def _wait_for_target(self, attempts=80):
        last = None
        for _ in range(attempts):
            try:
                with urllib.request.urlopen(
                    "http://127.0.0.1:%d/json/list" % self.port, timeout=2
                ) as resp:
                    targets = json.loads(resp.read().decode("utf-8"))
                for target in targets:
                    if target.get("type") == "page" and target.get("webSocketDebuggerUrl"):
                        return target["webSocketDebuggerUrl"]
            except Exception as exc:  # noqa: BLE001 - очікуємо готовності Chrome
                last = exc
            time.sleep(0.25)
        raise RuntimeError("Не вдалося підключитися до Chrome CDP: %s" % last)

    def stop(self):
        if self.ws:
            self.ws.close()
            self.ws = None
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            self.proc = None
        if self.profile and os.path.isdir(self.profile):
            shutil.rmtree(self.profile, ignore_errors=True)
            self.profile = None

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc):
        self.stop()
        return False

    # ---------- зручні обгортки ----------
    def navigate(self, url):
        self.console = []
        self.page_errors = []
        self.failed_requests = []
        self.send("Page.navigate", {"url": url})
        self.wait_for_load()
        return self

    def wait_for_load(self, timeout=20):
        deadline = time.time() + timeout
        while time.time() < deadline:
            state = self.evaluate("document.readyState")
            if state == "complete":
                time.sleep(0.3)
                return True
            time.sleep(0.1)
        return False

    def evaluate(self, expression):
        result = self.send(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True,
            },
        )
        if result.get("exceptionDetails"):
            details = result["exceptionDetails"]
            raise RuntimeError(
                "JS exception: %s %s"
                % (
                    details.get("text", ""),
                    details.get("exception", {}).get("description", ""),
                )
            )
        return result.get("result", {}).get("value")

    def set_viewport(self, width, height, mobile=False):
        self.send(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
                "mobile": mobile,
            },
        )

    def set_print_media(self, enabled=True):
        self.send(
            "Emulation.setEmulatedMedia",
            {"media": "print" if enabled else "screen"},
        )

    def reset_media(self):
        self.send("Emulation.setEmulatedMedia", {"media": ""})

    def clear_console(self):
        self.console = []
        self.page_errors = []
        self.failed_requests = []

    def send(self, method, params=None, timeout=None):
        self.msg_id += 1
        message_id = self.msg_id
        self.ws.send(
            json.dumps({"id": message_id, "method": method, "params": params or {}})
        )
        deadline = time.time() + (timeout or self.timeout)
        while time.time() < deadline:
            raw = self.ws.recv()
            if raw is None:
                continue
            try:
                message = json.loads(raw)
            except ValueError:
                continue
            if "method" in message:
                self._on_event(message)
                continue
            if message.get("id") == message_id:
                if "error" in message:
                    raise RuntimeError(
                        "%s failed: %s" % (method, message["error"].get("message"))
                    )
                return message.get("result", {})
        raise RuntimeError("Timeout waiting for %s" % method)

    def _on_event(self, message):
        method = message.get("method", "")
        params = message.get("params", {})
        if method == "Runtime.consoleAPICalled":
            level = params.get("type", "log")
            text = " ".join(
                str(arg.get("value", arg.get("description", "")))
                for arg in params.get("args", [])
            )
            self.console.append({"level": level, "text": text})
        elif method == "Runtime.exceptionThrown":
            details = params.get("exceptionDetails", {})
            self.page_errors.append(
                "%s %s"
                % (
                    details.get("text", "unknown exception"),
                    details.get("exception", {}).get("description", ""),
                )
            )
        elif method == "Log.entryAdded":
            entry = params.get("entry", {})
            if entry.get("level") in ("error", "warning"):
                self.console.append(
                    {"level": entry.get("level"), "text": entry.get("text", "")}
                )
        elif method == "Network.loadingFailed":
            self.failed_requests.append(
                {
                    "type": params.get("type"),
                    "errorText": params.get("errorText"),
                    "blockedReason": params.get("blockedReason"),
                }
            )
        elif method == "Network.responseReceived":
            response = params.get("response", {})
            if response.get("status", 200) >= 400:
                self.failed_requests.append(
                    {
                        "status": response.get("status"),
                        "url": response.get("url"),
                        "type": params.get("type"),
                    }
                )
