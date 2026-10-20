# PUBLIC_HTML_TEMPLATE.md — Публічний веб-портал ШІ-Медіаімперії (public.html)

Цей файл описує **Публічний Медіа-Портал** проєкту — зовнішній інструмент комунікації, трансляцій та мовлення для широкої аудиторії.

Скопіюйте наведений нижче HTML-код і збережіть його у папці вашого проєкту як **`public.html`**.

```html
<!DOCTYPE html>
<html lang="uk" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Медіаімперія — Офіційний Публічний Портал</title>
    <!-- Tailwind CSS CDN для $0 бюджету -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        imperial: { 900: '#1a0933', 800: '#2a124d', 500: '#8b5cf6', 400: '#a78bfa' }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-950 text-gray-100 min-h-screen font-sans antialiased">

    <!-- Публічний Header -->
    <header class="border-b border-imperial-800 bg-imperial-900/90 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <span class="text-3xl">📻</span>
                <div>
                    <h1 class="text-xl font-bold tracking-wide text-amber-400">ШІ-МЕДІАІМПЕРІЯ</h1>
                    <p class="text-xs text-gray-400">Офіційний публічний канал трансляції та новин</p>
                </div>
            </div>

            <!-- Режим Контурів та Вхід в Адмінку -->
            <div class="flex items-center gap-3">
                <div class="flex items-center bg-gray-900 p-1 rounded-lg border border-gray-800">
                    <button id="btn-tanunah" onclick="setContour('tanunah')" class="px-3 py-1 text-xs font-semibold bg-imperial-500 text-white rounded">
                        🌐 Tanunah (Метрополія)
                    </button>
                    <button id="btn-achtung" onclick="setContour('achtung')" class="px-3 py-1 text-xs font-semibold text-gray-400 hover:text-white rounded">
                        ⚠️ Achtung (Сатира)
                    </button>
                </div>
                <a href="index.html" class="px-3 py-1.5 text-xs font-bold bg-gray-800 hover:bg-gray-700 text-imperial-400 border border-imperial-500/30 rounded-lg flex items-center gap-1">
                    <span>🔒</span> Вхід в Канцелярію
                </a>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-8 space-y-8">

        <!-- Баннер Головної Трансляції / Радіо «Опричник» -->
        <section class="p-6 rounded-2xl bg-gradient-to-r from-amber-950/40 via-imperial-900/60 to-gray-900 border border-amber-500/30 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div class="space-y-2">
                <div class="flex items-center gap-2">
                    <span class="inline-block w-3 h-3 bg-red-500 rounded-full animate-ping"></span>
                    <span class="text-xs font-mono text-amber-400 uppercase tracking-wider font-bold">Прямий Ефір • Радіо «Опричник»</span>
                </div>
                <h2 class="text-2xl font-bold text-white">Трансляція Новин Канцелярії & Аналітичний Ефір</h2>
                <p id="public-desc" class="text-xs text-gray-300 max-w-2xl">
                    Офіційні матеріали від Новинаря, геополітична аналітика та публічні Директиви Української Імперії.
                </p>
            </div>
            <button class="px-5 py-3 bg-amber-500 hover:bg-amber-400 text-gray-950 font-bold rounded-xl text-sm shadow-lg shadow-amber-500/20 flex items-center gap-2">
                <span>▶</span> Увімкнути Радіоефір
            </button>
        </section>

        <!-- Публічна Стрічка Новин (Новинарь) -->
        <section class="space-y-4">
            <div class="flex justify-between items-center">
                <h3 class="text-lg font-bold text-gray-200 flex items-center gap-2">
                    <span>📰</span> Останні Публікації Новинаря
                </h3>
                <span class="text-xs text-gray-400">Синхронізовано з Канцелярією</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Картка Новини 1 -->
                <article class="p-5 rounded-xl bg-gray-900/90 border border-gray-800 space-y-3">
                    <div class="flex justify-between text-xs text-gray-400">
                        <span class="text-imperial-400 font-semibold">🏛️ Офіційна Директива</span>
                        <span>20 Жовтня 2026</span>
                    </div>
                    <h4 class="font-bold text-base text-gray-100">Затвердження Канону скасування областей та впровадження Країв</h4>
                    <p class="text-xs text-gray-300 leading-relaxed">
                        Канцелярія завершила перереєстрацію суб'єктів за автономерами та кодами ЗКАТО. Усі області скасовано з перетворенням на Народні Республіки або Края.
                    </p>
                </article>

                <!-- Картка Новини 2 -->
                <article class="p-5 rounded-xl bg-gray-900/90 border border-gray-800 space-y-3">
                    <div class="flex justify-between text-xs text-gray-400">
                        <span class="text-amber-400 font-semibold">🗺️ Аналітика Географа</span>
                        <span>19 Жовтня 2026</span>
                    </div>
                    <h4 class="font-bold text-base text-gray-100">Публікація Інтерактивної Ситуаційної Карти</h4>
                    <p class="text-xs text-gray-300 leading-relaxed">
                        Географ оприлюднив актуальну карту паспортів територій з інтеграцією Google My Maps та синонімами областей.
                    </p>
                </article>
            </div>
        </section>

        <!-- Публічна Вітрина Указів Канцелярії -->
        <section class="p-6 rounded-2xl bg-gray-900 border border-imperial-500/20 space-y-4">
            <h3 class="text-lg font-bold text-imperial-400 flex items-center gap-2">
                <span>📜</span> Публічний Реєстр Дзеркальних Указів
            </h3>
            <p class="text-xs text-gray-400">Перегляд монументальних указів, виданих Радою Оркестраторів для публічного ознайомлення.</p>
            <div class="p-4 rounded-lg bg-gray-950 border border-gray-800 text-xs text-gray-300 font-mono">
                [Указ №102] Про деколонізацію спадщини та повернення когнітивних стандартів до Києва.
            </div>
        </section>

    </main>

    <footer class="border-t border-gray-900 py-6 mt-12 text-center text-xs text-gray-500">
        Медіаімперія Української Імперії • $0 Static Deployment (GitHub Pages)
    </footer>

    <script>
        function setContour(c) {
            const t = document.getElementById('btn-tanunah');
            const a = document.getElementById('btn-achtung');
            const d = document.getElementById('public-desc');
            if (c === 'tanunah') {
                t.className = 'px-3 py-1 text-xs font-semibold bg-imperial-500 text-white rounded';
                a.className = 'px-3 py-1 text-xs font-semibold text-gray-400 hover:text-white rounded';
                d.innerText = 'Офіційні матеріали від Новинаря, геополітична аналітика та публічні Директиви Української Імперії.';
            } else {
                a.className = 'px-3 py-1 text-xs font-semibold bg-amber-600 text-white rounded';
                t.className = 'px-3 py-1 text-xs font-semibold text-gray-400 hover:text-white rounded';
                d.innerText = 'Гостра сатира, ефіри «Опричника» та розвінчання ворожих міфів.';
            }
        }
    </script>
</body>
</html>
```
