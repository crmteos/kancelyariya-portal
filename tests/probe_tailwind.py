"""Діагностика: як Tailwind Play CDN інжектить стилі у документ."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import Browser  # noqa: E402
from run_tests import BASE, start_server  # noqa: E402


def main():
    server = start_server()
    browser = Browser(headless=True)
    try:
        browser.start()
        browser.navigate(BASE + "/index.html")
        time.sleep(1.5)
        info = browser.evaluate(
            "JSON.stringify({"
            " styles: Array.from(document.querySelectorAll('style')).map(function (s) {"
            "   return {attrs: Array.from(s.attributes).map(function (a) { return a.name; }),"
            "          len: (s.textContent || '').length,"
            "          head: (s.textContent || '').slice(0, 200)};"
            " }),"
            " hasDataTw: !!document.querySelector('style[data-tailwind]'),"
            " twKeys: window.tailwind ? Object.keys(window.tailwind) : null,"
            " sheetCount: document.styleSheets.length,"
            " sheetRules: Array.from(document.styleSheets).map(function (sh) {"
            "   try { return sh.cssRules.length; } catch (e) { return 'blocked'; }"
            " })"
            "})"
        )
        print(info)
    finally:
        browser.stop()
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
