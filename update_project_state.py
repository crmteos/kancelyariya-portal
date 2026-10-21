import os

# Read the file
with open('c:\\kancelyariya-portal\\PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Update phase line
content = content.replace('Фаза 2 — Трикомпонентна верстка (Публічний Портал + Приватна Адмінка + Генератор Указів)', 'Фаза 2 — Розробка реляційних JSON-схем даних, OSINT-паспортів та ГІС-картографії')

# Update date line  
content = content.replace('20 жовтня 2026 р. (Версія 5 — Автотести на headless Chrome + Gemini-підсилення + CI/Pages)', '21 października 2026 р. (Версія 5 — Автотести на headless Chrome + Gemini-підсилення + CI/Pages)')

# Write back
with open('c:\\kancelyariya-portal\\PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated phase and date')