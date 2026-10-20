"""
run_tests.py — Автотести порталу «Канцелярія Української Імперії».

Стек: Python 3 (stdlib only) + headless Chrome через Chrome DevTools Protocol.
Жодних платних або сторонніх залежностей → $0 бюджет.

Запуск:
    python tests/run_tests.py            # усі тести
    python tests/run_tests.py index      # лише тести, у назві яких є "index"
    python tests/run_tests.py --headful  # з видимим вікном Chrome
"""

import functools
import http.server
import json
import os
import socket
import socketserver
import sys
import threading
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cdp import Browser  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8777
BASE = "http://127.0.0.1:%d" % PORT

GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"

TESTS = []


def test(name):
    """Реєструє тест-кейс."""

    def decorator(func):
        TESTS.append((name, func))
        return func

    return decorator


class Check(object):
    """Накопичує результати перевірок одного кейсу."""

    def __init__(self, name):
        self.name = name
        self.failures = []
        self.passed = 0

    def ok(self, condition, message, detail=""):
        if condition:
            self.passed += 1
        else:
            self.failures.append("%s%s" % (message, (" — " + str(detail)) if detail else ""))
        return bool(condition)

    def equal(self, actual, expected, message):
        return self.ok(actual == expected, message, "expected %r, got %r" % (expected, actual))

    def contains(self, haystack, needle, message):
        return self.ok(
            needle in (haystack or ""), message, "%r not in %r" % (needle, str(haystack)[:200])
        )

    def no_console_errors(self, browser, ignore_external=True):
        errors = [c for c in browser.console if c.get("level") == "error"]
        if ignore_external:
            errors = [
                e
                for e in errors
                if "cdn.tailwindcss.com" not in e.get("text", "")
                and "favicon" not in e.get("text", "")
            ]
        self.ok(not errors, "Немає помилок у консолі", errors)
        self.ok(not browser.page_errors, "Немає винятків у сторінці", browser.page_errors)


# ===================== Локальний HTTP-сервер =====================

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Статика з кореня проєкту + відсутність шуму в логах."""

    def log_message(self, fmt, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def handle_one_request(self):
        """Chrome обриває з'єднання без прощального запиту — це не помилка."""
        try:
            super().handle_one_request()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            self.close_connection = True


class ThreadedServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def start_server():
    handler = functools.partial(QuietHandler, directory=ROOT)
    server = ThreadedServer(("127.0.0.1", PORT), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    for _ in range(40):
        try:
            with socket.create_connection(("127.0.0.1", PORT), timeout=0.5):
                return server
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("Локальний HTTP-сервер не піднявся")


# ===================== Тест-кейси: index.html =====================

@test("index: базова структура та заголовки")
def test_index_structure(browser, check):
    browser.navigate(BASE + "/index.html")
    check.equal(browser.evaluate("document.title"), "Радіо «Опричник» — Публічний Медіа-Портал", "title коректний")
    check.equal(browser.evaluate("document.documentElement.lang"), "uk", "lang=uk")
    check.ok(browser.evaluate("!!document.querySelector('meta[name=viewport]')"), "є viewport meta")
    check.equal(
        browser.evaluate("document.querySelectorAll('#news-feed article').length"),
        6,
        "стрічка новин містить 6 матеріалів",
    )
    check.equal(
        browser.evaluate("document.querySelectorAll('#news-filters .news-filter').length"),
        5,
        "5 фільтрів категорій",
    )
    check.equal(
        browser.evaluate("document.querySelectorAll('#decrees-registry > div').length"),
        3,
        "реєстр указів містить 3 позиції",
    )
    check.no_console_errors(browser)


@test("index: перемикання світоглядних контурів")
def test_index_contours(browser, check):
    browser.navigate(BASE + "/index.html")
    tanunah_desc = browser.evaluate("document.getElementById('public-desc').innerText")
    check.contains(tanunah_desc, "Офіційні матеріали", "контур Tanunah активний за замовчуванням")
    check.equal(
        browser.evaluate("document.getElementById('btn-tanunah').getAttribute('aria-pressed')"),
        "true",
        "aria-pressed для Tanunah",
    )
    check.equal(browser.evaluate("document.body.getAttribute('data-contour')"), "tanunah", "data-contour=tanunah")

    browser.evaluate("setContour('achtung')")
    achtung_desc = browser.evaluate("document.getElementById('public-desc').innerText")
    check.contains(achtung_desc, "сатира", "контур Achtung змінює опис")
    check.ok(achtung_desc != tanunah_desc, "опис контуру фактично змінився")
    check.equal(browser.evaluate("document.body.getAttribute('data-contour')"), "achtung", "data-contour=achtung")
    check.equal(
        browser.evaluate("document.getElementById('btn-achtung').getAttribute('aria-pressed')"),
        "true",
        "aria-pressed для Achtung",
    )
    check.contains(
        browser.evaluate("document.getElementById('contour-badge').innerText"),
        "Сатира",
        "бейдж контуру оновлено",
    )
    check.no_console_errors(browser)


@test("index: фільтри стрічки новин")
def test_index_filters(browser, check):
    browser.navigate(BASE + "/index.html")
    browser.evaluate("document.querySelector('[data-cat=nauka]').click()")
    count = browser.evaluate("document.querySelectorAll('#news-feed article').length")
    check.equal(count, 1, "фільтр «Наука» залишає 1 картку")
    check.equal(
        browser.evaluate("document.getElementById('news-empty').classList.contains('hidden')"),
        True,
        "порожній стан приховано",
    )
    browser.evaluate("document.querySelector('[data-cat=all]').click()")
    check.equal(
        browser.evaluate("document.querySelectorAll('#news-feed article').length"),
        6,
        "повернення до «Усі» показує 6 карток",
    )
    check.no_console_errors(browser)


@test("index: прямий ефір (toggleLive)")
def test_index_live(browser, check):
    browser.navigate(BASE + "/index.html")
    check.equal(
        browser.evaluate("document.getElementById('live-indicator').classList.contains('hidden')"),
        True,
        "індикатор ефіру приховано на старті",
    )
    browser.evaluate("toggleLive()")
    check.equal(
        browser.evaluate("document.getElementById('live-indicator').classList.contains('hidden')"),
        False,
        "індикатор ефіру показано",
    )
    check.equal(
        browser.evaluate("document.getElementById('live-label').innerText"),
        "Зупинити Радіоефір",
        "підпис кнопки змінено",
    )
    browser.evaluate("toggleLive()")
    check.equal(
        browser.evaluate("document.getElementById('live-indicator').classList.contains('hidden')"),
        True,
        "ефір зупинено",
    )
    check.no_console_errors(browser)


# ===================== Тест-кейси: admin.html =====================

@test("admin: базова структура приватної панелі")
def test_admin_structure(browser, check):
    browser.navigate(BASE + "/admin.html")
    check.equal(
        browser.evaluate("document.title"),
        "ШІ-Канцелярія — Приватна Панель Керування",
        "title коректний",
    )
    check.equal(
        browser.evaluate("document.querySelectorAll('.accordion-item').length"),
        4,
        "4 вузли ШІ-Канцелярії",
    )
    check.equal(
        browser.evaluate("document.querySelectorAll('#agent-list li').length"),
        4,
        "4 вузли у списку на зв'язку",
    )
    check.ok(
        browser.evaluate("document.querySelector('meta[name=robots]').content.includes('noindex')"),
        "приватна сторінка закрита від індексації",
    )
    check.no_console_errors(browser)


@test("admin: акордеони вузлів")
def test_admin_accordions(browser, check):
    browser.navigate(BASE + "/admin.html")
    check.equal(
        browser.evaluate("document.getElementById('acc-novynar').classList.contains('hidden')"),
        True,
        "вузол згорнутий за замовчуванням",
    )
    browser.evaluate("toggleAccordion('acc-novynar')")
    check.equal(
        browser.evaluate("document.getElementById('acc-novynar').classList.contains('hidden')"),
        False,
        "вузол розгорнуто",
    )
    check.equal(
        browser.evaluate(
            "document.querySelector('.accordion-item[data-node=novynar] .accordion-header')"
            ".getAttribute('aria-expanded')"
        ),
        "true",
        "aria-expanded коректний",
    )
    browser.evaluate("toggleAccordion('acc-novynar')")
    check.equal(
        browser.evaluate("document.getElementById('acc-novynar').classList.contains('hidden')"),
        True,
        "вузол згорнуто повторно",
    )
    check.no_console_errors(browser)


@test("admin: розгортання/згортання всіх вузлів")
def test_admin_expand_all(browser, check):
    browser.navigate(BASE + "/admin.html")
    browser.evaluate("expandAll(true)")
    visible = browser.evaluate(
        "Array.from(document.querySelectorAll('.accordion-body'))"
        ".filter(function (b) { return !b.classList.contains('hidden'); }).length"
    )
    check.equal(visible, 4, "expandAll(true) розгортає всі 4 вузли")
    browser.evaluate("expandAll(false)")
    visible = browser.evaluate(
        "Array.from(document.querySelectorAll('.accordion-body'))"
        ".filter(function (b) { return !b.classList.contains('hidden'); }).length"
    )
    check.equal(visible, 0, "expandAll(false) згортає всі вузли")
    check.no_console_errors(browser)


@test("admin: журнал подій")
def test_admin_log(browser, check):
    browser.navigate(BASE + "/admin.html")
    initial = browser.evaluate("document.querySelectorAll('#event-log li').length")
    check.ok(initial >= 2, "журнал містить стартові записи", initial)
    browser.evaluate("logEvent('Тестовий запис')")
    check.equal(
        browser.evaluate("document.querySelectorAll('#event-log li').length"),
        initial + 1,
        "журнал поповнюється",
    )
    check.contains(
        browser.evaluate("document.getElementById('event-log').innerText"),
        "Тестовий запис",
        "текст запису присутній",
    )
    browser.evaluate("clearLog()")
    check.equal(
        browser.evaluate("document.querySelectorAll('#event-log li').length"),
        1,
        "після очищення лишається лише запис про очищення",
    )
    check.no_console_errors(browser)


# ===================== Тест-кейси: decrees.html =====================

@test("decrees: базова структура генератора")
def test_decrees_structure(browser, check):
    browser.navigate(BASE + "/decrees.html")
    check.contains(browser.evaluate("document.title"), "Генератор Дзеркальних Указів", "title коректний")
    for field in ("in-region", "in-title", "in-officials", "in-bottlenecks", "in-number", "in-date"):
        check.ok(
            browser.evaluate("!!document.getElementById('%s')" % field),
            "поле %s присутнє" % field,
        )
    check.equal(
        browser.evaluate("!!document.getElementById('in-date').value"),
        True,
        "дата ініціалізована поточним днем",
    )
    check.no_console_errors(browser)


@test("decrees: генерація у двох контурах")
def test_decrees_generation(browser, check):
    browser.navigate(BASE + "/decrees.html")
    browser.evaluate("setContour('tanunah'); generateDecree();")
    tanunah_heading = browser.evaluate("document.getElementById('out-heading').innerText")
    check.contains(tanunah_heading, "ДИРЕКТИВА", "контур Tanunah → Стратегічна Директива")
    tanunah_body = browser.evaluate("document.getElementById('out-body').innerText")
    check.contains(tanunah_body, "постановляє", "текст Tanunah містить формулу указу")

    browser.evaluate("setContour('achtung'); generateDecree();")
    achtung_heading = browser.evaluate("document.getElementById('out-heading').innerText")
    check.contains(achtung_heading, "УКАЗ", "контур Achtung → Дзеркальний Указ")
    check.ok(achtung_heading != tanunah_heading, "заголовки контурів відрізняються")
    check.contains(
        browser.evaluate("document.getElementById('out-body').innerText"),
        "настоящим уведомляет",
        "текст Achtung містить сатиричну формулу",
    )
    check.no_console_errors(browser)


@test("decrees: топоніми та внесення даних у текст")
def test_decrees_data(browser, check):
    browser.navigate(BASE + "/decrees.html")
    browser.evaluate(
        "document.getElementById('in-region').value = 'SAMARA';"
        "document.getElementById('in-title').value = 'Тестовий заголовок указу';"
        "document.getElementById('in-officials').value = 'Мер Тестового Міста; Губернатор';"
        "document.getElementById('in-bottlenecks').value = 'Прорив труби; Борг перед житловиками';"
        "document.getElementById('in-number').value = '№777';"
        "setContour('tanunah'); generateDecree();"
    )
    body = browser.evaluate("document.getElementById('out-body').innerText")
    check.contains(body, "Самарський край", "код SAMARA розгорнуто в топонім")
    check.contains(body, "Мер Тестового Міста", "посади смотрящих вбудовано")
    check.contains(body, "Прорив труби", "больові точки вбудовано")
    check.contains(body, "Борг перед житловиками", "другий пункт больових точок вбудовано")
    check.contains(
        browser.evaluate("document.getElementById('out-meta').innerText"),
        "№777",
        "номер указу відображено",
    )
    check.no_console_errors(browser)


@test("decrees: архів у localStorage")
def test_decrees_archive(browser, check):
    browser.navigate(BASE + "/decrees.html")
    browser.evaluate("localStorage.removeItem('chancery_decrees_archive'); renderArchive();")
    check.equal(
        browser.evaluate("document.getElementById('archive-count').innerText"),
        "0",
        "архів порожній після очищення",
    )
    browser.evaluate("generateDecree();")
    browser.evaluate("generateDecree();")
    check.equal(
        browser.evaluate("document.getElementById('archive-count').innerText"),
        "2",
        "архів накопичує 2 записи",
    )
    check.equal(
        browser.evaluate("document.querySelectorAll('#archive-list li').length"),
        2,
        "список архіву містить 2 позиції",
    )
    stored = browser.evaluate(
        "JSON.parse(localStorage.getItem('chancery_decrees_archive') || '[]').length"
    )
    check.equal(stored, 2, "записи збережено в localStorage")
    browser.evaluate("clearArchive();")
    check.equal(
        browser.evaluate("document.getElementById('archive-count').innerText"),
        "0",
        "кнопка очищення скидає архів",
    )
    check.no_console_errors(browser)


@test("decrees: Gemini — панель керування ключем")
def test_decrees_gemini_panel(browser, check):
    browser.navigate(BASE + "/decrees.html")
    check.ok(
        browser.evaluate("!!document.getElementById('gemini-enabled')"),
        "є перемикач увімкнення Gemini",
    )
    check.ok(
        browser.evaluate("!!document.getElementById('gemini-key')"),
        "є поле введення API-ключа",
    )
    check.equal(
        browser.evaluate("document.getElementById('gemini-key').type"),
        "password",
        "поле ключа приховане (type=password)",
    )
    check.equal(
        browser.evaluate("document.getElementById('gemini-key').autocomplete"),
        "off",
        "autocomplete вимкнено для поля ключа",
    )
    check.equal(browser.evaluate("geminiEnabled"), False, "Gemini вимкнено за замовчуванням")
    check.equal(browser.evaluate("geminiKey"), "", "ключ порожній за замовчуванням")
    check.contains(
        browser.evaluate("document.getElementById('gemini-status').innerText"),
        "офлайн-генератор",
        "статус за замовчуванням повідомляє про офлайн-генератор",
    )
    check.no_console_errors(browser)


@test("decrees: Gemini — ключ не потрапляє у сховище")
def test_decrees_gemini_no_persistence(browser, check):
    browser.navigate(BASE + "/decrees.html")
    browser.evaluate(
        "document.getElementById('gemini-key').value = 'AIzaTESTKEY-not-real';"
        "saveGeminiKey();"
    )
    check.equal(
        browser.evaluate("geminiKey"),
        "AIzaTESTKEY-not-real",
        "ключ прийнято у змінну пам'яті",
    )
    stored = browser.evaluate(
        "JSON.stringify({ls: Object.keys(localStorage), ss: Object.keys(sessionStorage)})"
    )
    check.ok(
        "AIzaTESTKEY-not-real" not in stored,
        "ключ відсутній у localStorage/sessionStorage",
        stored,
    )
    # Перезавантаження сторінки стирає ключ.
    browser.navigate(BASE + "/decrees.html")
    check.equal(browser.evaluate("geminiKey"), "", "після перезавантаження ключ зник")
    check.equal(
        browser.evaluate("document.getElementById('gemini-key').value"),
        "",
        "поле ключа порожнє після перезавантаження",
    )
    # Кнопка очищення теж скидає ключ.
    browser.evaluate(
        "document.getElementById('gemini-key').value = 'AIzaANOTHER'; saveGeminiKey();"
    )
    browser.evaluate("clearGeminiKey();")
    check.equal(browser.evaluate("geminiKey"), "", "кнопка очищення скидає ключ")
    check.equal(
        browser.evaluate("document.getElementById('gemini-key').value"),
        "",
        "поле ключа очищено",
    )
    check.no_console_errors(browser)


@test("decrees: Gemini — увімкнення розблоковує панель")
def test_decrees_gemini_toggle(browser, check):
    browser.navigate(BASE + "/decrees.html")
    browser.evaluate("setGeminiEnabled(true);")
    check.equal(browser.evaluate("geminiEnabled"), True, "Gemini увімкнено")
    check.ok(
        "pointer-events-none"
        not in browser.evaluate("document.getElementById('gemini-panel').className"),
        "панель активна (pointer-events-none знято)",
    )
    check.contains(
        browser.evaluate("document.getElementById('gemini-status').innerText"),
        "Введіть API-ключ",
        "статус просить ввести ключ",
    )
    browser.evaluate("setGeminiEnabled(false);")
    check.equal(browser.evaluate("geminiEnabled"), False, "Gemini вимкнено")
    check.ok(
        "pointer-events-none"
        in browser.evaluate("document.getElementById('gemini-panel').className"),
        "панель знову заблокована",
    )
    check.no_console_errors(browser)


@test("decrees: Gemini — помилка API переходить на офлайн-генератор")
def test_decrees_gemini_fallback(browser, check):
    browser.navigate(BASE + "/decrees.html")
    browser.evaluate("localStorage.removeItem('chancery_decrees_archive'); renderArchive();")
    # Підміняємо fetch, щоб не робити живих викликів до Google API.
    browser.evaluate(
        "window.__geminiCalls = [];"
        "window.__origFetch = window.fetch;"
        "window.fetch = function (url, opts) {"
        "  window.__geminiCalls.push({url: String(url), method: opts && opts.method});"
        "  return Promise.resolve({ok: false, status: 400,"
        "    json: function () { return Promise.resolve({error: {message: 'API key not valid'}}); }"
        "  });"
        "};"
    )
    browser.evaluate(
        "document.getElementById('gemini-key').value = 'AIzaFAKE';"
        "saveGeminiKey();"
        "setGeminiEnabled(true);"
    )
    outcome = browser.evaluate("generateDecreeWithGemini()")
    check.equal(outcome, "fallback", "помилка API → офлайн-фолбек")
    body = browser.evaluate("document.getElementById('out-body').innerText")
    check.contains(body, "постановляє", "офлайн-указ згенеровано після помилки Gemini")
    status = browser.evaluate("document.getElementById('gemini-status').innerText")
    check.contains(status, "API key not valid", "статус показує причину помилки")
    check.contains(status, "офлайн", "статус повідомляє про фолбек")
    check.equal(
        browser.evaluate("document.getElementById('archive-count').innerText"),
        "1",
        "указ потрапив в архів",
    )
    calls = browser.evaluate("window.__geminiCalls")
    check.equal(len(calls), 1, "виконано рівно один запит до Gemini")
    check.ok(
        calls and "generativelanguage.googleapis.com" in calls[0]["url"],
        "запит адресовано до Gemini API",
        calls,
    )
    check.ok(
        calls and "key=AIzaFAKE" in calls[0]["url"],
        "ключ передано параметром запиту",
        calls,
    )
    browser.evaluate("window.fetch = window.__origFetch;")
    check.no_console_errors(browser)


@test("decrees: Gemini — успішна відповідь API рендериться як указ")
def test_decrees_gemini_success(browser, check):
    browser.navigate(BASE + "/decrees.html")
    browser.evaluate("localStorage.removeItem('chancery_decrees_archive'); renderArchive();")
    browser.evaluate(
        "window.fetch = function () {"
        "  return Promise.resolve({ok: true, status: 200,"
        "    json: function () { return Promise.resolve({candidates: [{content: {parts: ["
        "      {text: 'ПОСТАНОВЛЯЄ:\\n\\nПункт перший.\\n\\nПункт другий.'}"
        "    ]}}]}); }"
        "  });"
        "};"
    )
    browser.evaluate(
        "document.getElementById('gemini-key').value = 'AIzaFAKE';"
        "saveGeminiKey();"
        "setGeminiEnabled(true);"
        "setContour('tanunah');"
    )
    outcome = browser.evaluate("generateDecreeWithGemini()")
    check.equal(outcome, "gemini", "успішна відповідь Gemini прийнята")
    body = browser.evaluate("document.getElementById('out-body').innerText")
    check.contains(body, "ПОСТАНОВЛЯЄ", "текст Gemini виведено на папір")
    check.contains(body, "Пункт другий", "другий абзац Gemini присутній")
    check.contains(
        browser.evaluate("document.getElementById('gen-status').innerText"),
        "Gemini",
        "статус генерації повідомляє про Gemini",
    )
    check.contains(
        browser.evaluate("document.getElementById('gemini-status').innerText"),
        "✓",
        "статус Gemini позначає успіх",
    )
    check.no_console_errors(browser)


@test("decrees: Gemini — HTML у відповіді екранується")
def test_decrees_gemini_escaping(browser, check):
    browser.navigate(BASE + "/decrees.html")
    browser.evaluate(
        "window.fetch = function () {"
        "  return Promise.resolve({ok: true, status: 200,"
        "    json: function () { return Promise.resolve({candidates: [{content: {parts: ["
        "      {text: '<img src=x onerror=window.__pwned=true>Опис указу'}"
        "    ]}}]}); }"
        "  });"
        "};"
    )
    browser.evaluate(
        "document.getElementById('gemini-key').value = 'AIzaFAKE';"
        "saveGeminiKey();"
        "setGeminiEnabled(true);"
    )
    browser.evaluate("generateDecreeWithGemini()")
    check.equal(
        browser.evaluate("window.__pwned === undefined"),
        True,
        "ін'єктований обробник не виконався",
    )
    check.equal(
        browser.evaluate("document.querySelectorAll('#out-body img').length"),
        0,
        "тег <img> екрановано (не вставлено в DOM)",
    )
    check.contains(
        browser.evaluate("document.getElementById('out-body').innerText"),
        "Опис указу",
        "корисний текст відповіді збережено",
    )
    check.no_console_errors(browser)


@test("public: redirect-stub на index.html")
def test_public_redirect(browser, check):
    browser.navigate(BASE + "/public.html")
    time.sleep(0.6)
    check.ok(
        browser.evaluate("location.pathname").endswith("/index.html"),
        "public.html перенаправляє на index.html",
        browser.evaluate("location.pathname"),
    )
    check.equal(
        browser.evaluate("document.title"),
        "Радіо «Опричник» — Публічний Медіа-Портал",
        "після редиректу завантажено публічний портал",
    )


# ===================== Тест-кейси: адаптивність і друк =====================

PAGES = ("index.html", "admin.html", "decrees.html")


@test("responsive: немає горизонтального переповнення (мобільний 375px)")
def test_responsive_mobile(browser, check):
    for page in PAGES:
        browser.set_viewport(375, 812, mobile=True)
        browser.navigate(BASE + "/" + page)
        overflow = browser.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        check.ok(
            overflow <= 1,
            "%s: без горизонтальної прокрутки на 375px" % page,
            "overflow=%spx" % overflow,
        )


@test("responsive: немає горизонтального переповнення (планшет 768px)")
def test_responsive_tablet(browser, check):
    for page in PAGES:
        browser.set_viewport(768, 1024)
        browser.navigate(BASE + "/" + page)
        overflow = browser.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        check.ok(
            overflow <= 1,
            "%s: без горизонтальної прокрутки на 768px" % page,
            "overflow=%spx" % overflow,
        )
    browser.set_viewport(1280, 1024)


@test("responsive: ключові блоки займають ширину екрана (desktop 1280px)")
def test_responsive_desktop(browser, check):
    browser.set_viewport(1280, 1024)
    for page in PAGES:
        browser.navigate(BASE + "/" + page)
        width = browser.evaluate("document.documentElement.clientWidth")
        main_width = browser.evaluate(
            "document.querySelector('main').getBoundingClientRect().width"
        )
        check.ok(
            main_width <= width and main_width > width * 0.5,
            "%s: головний контейнер займає більшість ширини" % page,
            "main=%spx viewport=%spx" % (main_width, width),
        )


@test("print: decrees.html ховає форму та показує папір")
def test_print_decrees(browser, check):
    browser.set_viewport(1280, 1024)
    browser.navigate(BASE + "/decrees.html")
    browser.evaluate("generateDecree();")
    browser.set_print_media(True)
    time.sleep(0.2)
    form_hidden = browser.evaluate(
        "getComputedStyle(document.querySelector('section.no-print')).display"
    )
    check.equal(form_hidden, "none", "форма входу прихована під час друку")
    paper_color = browser.evaluate(
        "getComputedStyle(document.getElementById('decree-paper')).color"
    )
    check.equal(paper_color, "rgb(0, 0, 0)", "папір друкується чорним текстом")
    browser.reset_media()
    time.sleep(0.2)
    form_back = browser.evaluate(
        "getComputedStyle(document.querySelector('section.no-print')).display"
    )
    check.ok(form_back != "none", "після виходу з друку форма видима")


@test("print: index.html та admin.html мають коректний друк")
def test_print_other_pages(browser, check):
    browser.set_viewport(1280, 1024)
    for page in ("index.html", "admin.html"):
        browser.navigate(BASE + "/" + page)
        browser.set_print_media(True)
        time.sleep(0.2)
        body_bg = browser.evaluate("getComputedStyle(document.body).backgroundColor")
        check.ok(
            body_bg in ("rgb(255, 255, 255)", "rgba(0, 0, 0, 0)", "transparent"),
            "%s: під час друку тло світле" % page,
            body_bg,
        )
        browser.reset_media()
        time.sleep(0.2)


# ===================== Тест-кейси: цілісність посилань =====================

@test("links: всі внутрішні посилання ведуть на наявні файли")
def test_internal_links(browser, check):
    browser.set_viewport(1280, 1024)
    for page in PAGES:
        browser.navigate(BASE + "/" + page)
        links = browser.evaluate(
            "Array.from(document.querySelectorAll('a[href]'))"
            ".map(function (a) { return a.getAttribute('href'); })"
        )
        for href in links:
            if not href or href.startswith(("http://", "https://", "#", "mailto:", "tel:")):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            status = browser.evaluate(
                "fetch('%s', {method: 'HEAD'}).then(function (r) { return r.status; })"
                % target
            )
            check.ok(
                status == 200,
                "%s → %s існує" % (page, target),
                "HTTP %s" % status,
            )


@test("links: зовнішні ресурси доступні (Tailwind CDN)")
def test_external_assets(browser, check):
    browser.navigate(BASE + "/index.html")
    # fetch() до CDN падає через CORS, тому перевіряємо, що Tailwind реально
    # застосував стилі (інакше всі кольори та розкладка лишились би дефолтними).
    body_bg = browser.evaluate("getComputedStyle(document.body).backgroundColor")
    check.equal(body_bg, "rgb(3, 7, 18)", "Tailwind CDN застосував тему (bg-gray-950)")
    heading_color = browser.evaluate(
        "getComputedStyle(document.querySelector('h1')).color"
    )
    check.equal(heading_color, "rgb(251, 191, 36)", "кастомний колір oprichnik-400 застосовано")
    # Play CDN додає <style> без атрибута data-tailwind, тому перевіряємо
    # наявність сгенерованих правил у document.styleSheets, а не маркер.
    rule_count = browser.evaluate(
        "Array.from(document.styleSheets).reduce(function (sum, sheet) {"
        "  try { return sum + sheet.cssRules.length; } catch (e) { return sum; }"
        "}, 0)"
    )
    check.ok(rule_count > 50, "Tailwind вставив сгенеровані стилі в документ", rule_count)
    tw_present = browser.evaluate(
        "!!(window.tailwind && window.tailwind.config && window.tailwind.config.theme)"
    )
    check.ok(tw_present, "tailwind.config прийнято та застосовано")


# ===================== Головний цикл =====================

def main(argv):
    headful = "--headful" in argv
    filters = [a for a in argv if not a.startswith("--")]

    selected = TESTS
    if filters:
        selected = [
            (name, func)
            for name, func in TESTS
            if any(f.lower() in name.lower() for f in filters)
        ]
        if not selected:
            print("Не знайдено тестів за фільтром: %s" % ", ".join(filters))
            return 2

    server = start_server()
    browser = Browser(headless=not headful)
    total_checks = 0
    failed_cases = []
    report = []

    try:
        browser.start()
        for name, func in selected:
            check = Check(name)
            try:
                func(browser, check)
            except Exception as exc:  # noqa: BLE001 - тест не має крашити раннер
                check.failures.append("Виняток: %s" % exc)
                if os.environ.get("CHANCERY_TRACE"):
                    traceback.print_exc()
            total_checks += check.passed + len(check.failures)
            if check.failures:
                failed_cases.append(check)
                line = "FAIL %s" % name
                report.append(line)
                for failure in check.failures:
                    report.append("      - %s" % failure)
                    print("      - %s" % failure)
            else:
                line = "PASS %s (%d перевірок)" % (name, check.passed)
                report.append(line)
            print("%s %s" % (line.split(" ")[0], line[5:]))
            _flush_report(report)
    finally:
        browser.stop()
        server.shutdown()
        server.server_close()

    summary = ""
    passed = len(selected) - len(failed_cases)
    if failed_cases:
        summary = "ПІДСУМОК: %d/%d тестів пройдено, перевірок: %d" % (
            passed, len(selected), total_checks
        )
    else:
        summary = "ПІДСУМОК: усі %d тестів пройдено (%d перевірок)" % (
            len(selected), total_checks
        )
    report.append(summary)
    _flush_report(report)

    print("")
    print(summary)
    return 1 if failed_cases else 0


def _flush_report(lines):
    """Пише звіт у файл одразу після кожного тесту (стійкість до переривання)."""
    path = os.environ.get("CHANCERY_REPORT", os.path.join(ROOT, "tests", "last_report.txt"))
    try:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
    except OSError:
        pass


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
