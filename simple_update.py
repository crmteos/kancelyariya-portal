import os

# Read the file
with open('c:\\kancelyariya-portal\\PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

print("File read successfully, length:", len(content))

# 1. Add Stage 1.1 after Stage 1
# Find Stage 1 and add 1.1 after it
if '| **Етап 1** | Впорядкування матеріалів' in content:
    # Find this line and add stage 1.1 after it
    idx = content.find('| **Етап 1** | Впорядкування матеріалів')
    if idx != -1:
        # Find the end of this line (next |)
        line_end = content.find('|', idx + 1)
        if line_end != -1:
            # Insert stage 1.1 after this line
            stage11 = '\n| **Етап 1.1** | Формування реляційної JSON-архітектури, ролі Смотрящого Атамана та Картографа — ✅ Завершено |'
            content = content[:line_end+1] + stage11 + content[line_end+1:]
            print("Added Stage 1.1")
        else:
            print("Could not find end of Stage 1 line")
    else:
        print("Could not find Stage 1 line")
else:
    print("Stage 1 pattern not found")

# 2. Stage 3 should already be updated (old text not found)
# Verify Stage 3 has the new text
if 'Інтеграція JSON-паспортів та Google My Maps' in content:
    print("Stage 3 has new text (integration)")
else:
    print("Stage 3 text check - may need updating")

# 3. Update Active Task
# Check for old active task text
old_task = 'Завдання:** ✅ **Виконано (Версії 5)**'
if old_task in content:
    # Replace it
    content = content.replace(
        'Завдання:** ✅ **Виконано (Версії 5)** — надійна валідація, Gemini-підсилення та підготовка до публікації на GitHub Pages.',
        'Завдання:** створення базових JSON-шаблонів regions_register.json та {region_code}_osint_passport.json.**'
    )
    print("Updated Active Task")
else:
    # Check if already updated
    if 'створення базових JSON-шаблонів' in content:
        print("Active Task already updated")
    else:
        print("Active Task text pattern not found")

# 4. Add Plans section - find a good location
# Look for the navigation matrix end or the limitations section
# Insert after the Active Task section

# Find "---" that separates sections after active task
# or find the "Створені та змінені файли" section
if 'Створені та змінені файли' in content:
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
    marker = 'Створені та змінені файли'
    idx = content.find(marker)
    if idx != -1:
        # Find the line start
        line_start = content.rfind('\n', 0, idx)
        if line_start == -1:
            line_start = 0
        # Insert the goals section before the marker
        content = content[:line_start] + goals_section + content[line_start:]
        print("Added Plans section")
    else:
        print("Could not find marker for goals section")

# 5. Ensure date is updated
content = content.replace(
    '20 жовтня 2026 р. (Версія 5 — Автотести на headless Chrome + Gemini-підсилення + CI/Pages)',
    '21 października 2026 р. (Версія 5 — Автотести на headless Chrome + Gemini-підсилення + CI/Pages)'
)

# 6. Ensure phase is updated
content = content.replace(
    'Фаза 2 — Трикомпонентна верстка (Публічний Портал + Приватна Адмінка + Генератор Указів)',
    'Фаза 2 — Розробка реляційних JSON-схем даних, OSINT-паспортів та ГІС-картографії'
)

# 7. Write the updated content back
with open('c:\\kancelyariya-portal\\PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFull update completed!")