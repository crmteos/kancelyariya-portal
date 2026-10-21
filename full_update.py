import re

# Read the file
with open('c:\\kancelyariya-portal\\PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

updated = True

# 1. Add Stage 1.1 after Stage 1 in the stages table
# Look for the pattern: | **Етап 1** | V latta | ✅ Завершено |
stage1_pattern = r'(\| \*\*Етап 1\*\* \| Впорядкування матеріалів у підпапках та зафіксування структуру \(`CHANCERY_STRUCTURE.md`\) \| ✅ Завершено \|)'
stage11_insert = r'\1\n| **Етап 1.1** | Формування реляційної JSON-архітектури, ролі Смотрящого Атамана та Картографа — ✅ Завершено |'

new_content = re.sub(
    r'(\| \*\*Етап 1\*\* \| Впорядкування матеріалів у підпапках та зафіксування структуру \(`CHANCERY_STRUCTURE.md`\) \| ✅ Завершено \|)',
    r'\1\n| **Етап 1.1** | Формування реляційної JSON-архітектури, ролі Смотрящого Атамана та Картографа — ✅ Завершено |',
    content
)

if new_content != content:
    content = new_content
    print("Added Stage 1.1")
else:
    print("Stage 1.1 pattern not found, trying alternative...")
    # Try alternative pattern
    if '| **Етап 1** | Впорядкування матеріалів' in content and '✅ Завершено |' in content:
        # Insert after stage 1
        idx = content.find('| **Етап 1** | Впорядкування матеріалів')
        if idx != -1:
            # Find the end of this line
            line_end = content.find('|', idx + 50)
            if line_end != -1:
                insertion = '\n| **Етап 1.1** | Формування реляційної JSON-архітектури, ролі Смотрящого Атамана та Картографа — ✅ Завершено |'
                content = content[:line_end+1] + insertion + content[line_end+1:]
                print("Added Stage 1.1 (alternative method)")
                updated = True

# 2. Update Stage 3 - it seems this was already done (old text not found)
# Check and add the new Stage 3 if needed
if 'Інтеграція JSON-паспортів та Google My Maps' not in content:
    if 'Розгортання безкоштовного хостингу' in content:
        # Replace stage 3
        stage3_old = '| **Етап 3** | Інтеграція JSON-паспортів та Google My Maps — ⏳ У процесі |'
        # This may already be there, check
        stage3_pattern = r'\| \*\*Етап 3\*\* \| [^\|]+\|'
        # Actually, let's just ensure it's there
        print("Checking Stage 3...")
    else:
        print("Stage 3 already updated (old text not found)")

# 3. Update Active Task
active_task_old = '**Завдання:** ✅ **Виконано (Версія 5)** — надійна валідація, Gemini-підсилення та підготовка до публікації на GitHub Pages.'
active_task_new = '**Завдання:** створення базових JSON-шаблонів regions_register.json та {region_code}_osint_passport.json.'

if re.search(active_task_old, content, re.DOTALL):
    content = content.replace(active_task_old, active_task_new)
    print("Updated Active Task")
    updated = True
else:
    print("Active Task pattern not found (may already be updated)")

# 4. Add/Update "Плани наступних цілей" section
# Since the goals section wasn't found, we need to add it
# Find the --- after Active Task section and insert before it
# Look for the Active Task section end and the navigation matrix

# First, find where to insert the goals section
# It should be after the Active Task and before the "---" separator that leads to the stages

# Check if there's a section we can replace
if '### Створені та змінені файли (Версія' in content:
    # Insert the goals section before this marker
    goals_section = '''
## ⏭️ Плани наступних цілей, задач і робіт

1. **Реалізація Схем JSON в Excel-стилі**:
   - Створити `regions_register.json` із первинними ключами `region_code` (коди автономерів/ЗКАТО).
   - Створити шаблон OSINT-паспорта для Смотрящих Атаманів з полями для стану інфраструктури, «поганял» та оперативних сигналів.
2. **Інтеграція з Гугл Картою Імперії**:
   - Підключити карту `https://www.google.com/maps/d/u/0/edit?mid=1nVz5dLwrxEYS3dWcCXfMU2z9-6GubpE` у блок Географа/Картографа.
   - Налаштувати стикування: зчитування гео-полів із JSON-паспорта та відображення відповідних точок/шарів у картографічному інтерфейсі.
   - Автогенерація указів із даних OSINT-паспортів для Канцелярії.
3. **Генератор Указів (`decreases.html`)**:
   - Налаштувати зчитування даних із JSON-паспорта Смотрящого Атамана для автогенерації повнотекстових указів Канцелярії.

'''
    # Find the marker and insert before it
    marker = '### Створені та змінені файли (Версії'
    idx = content.find(marker)
    if idx != -1:
        # Find the line start
        line_start = content.rfind('\n', 0, idx)
        if line_start == -1:
            line_start = 0
        # Insert the goals section before the marker
        content = content[:line_start] + goals_section + content[line_start:]
        print("Added Plans section before file list")
        updated = True
    else:
        print("Could not find marker for goals section insertion")

# 5. Update the date if needed (should already be done)
content = content.replace(
    '20 жовтня 2026 р. (Версія 5 — Автотести на headless Chrome + Gemini-підсилення + CI/Pages)',
    '21 października 2026 р. (Версія 5 — Автотести на headless Chrome + Gemini-підсилення + CI/Pages)'
)

# 6. Update phase if needed
content = content.replace(
    'Фаза 2 — Трикомпонентна верстка (Публічний Портал + Приватна Адмінка + Генератор Указів)',
    'Фаза 2 — Розробка реляційних JSON-схем даних, OSINT-паспортів та ГІС-картографії'
)

# 7. Write the updated content back
with open('c:\\kancelyariya-portal\\PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFull update completed!")