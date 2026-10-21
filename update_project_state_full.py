import os
import re

# Read the file
with open('c:\\kancelyariya-portal\\PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update phase line - already done, but let's ensure it's correct
content = content.replace(
    'Фаза 2 — Трикомпонентна верстка (Публічний Портал + Приватна Адмінка + Генератор Указів)',
    'Фаза 2 — Розробка реляційних JSON-схем даних, OSINT-паспортів та ГІС-картографії'
)

# 2. Update date line - already done, but let's ensure it's correct  
content = content.replace(
    '20 жовтня 2026 р. (Версія 5 — Автотести на headless Chrome + Gemini-підсилення + CI/Pages)',
    '21 października 2026 р. (Версія 5 — Автотести на headless Chrome + Gemini-підсилення + CI/Pages)'
)

# 3. Add Stage 1.1 after Stage 1 entry in the stages table
# We need to insert it after the Etap 1 line
stage1_pattern = '| **Етап 1** | Впорядкування матеріалів у підпапках та зафіксування структури (`CHANCERY_STRUCTURE.md`) | ✅ Завершено |'
stage11_addition = '| **Етап 1.1** | Формування реляційної JSON-архітектури, ролі Смотрящого Атамана та Картографа — ✅ Завершено |'

# Insert Stage 1.1 after Stage 1
content = content.replace(stage1_pattern, stage1_pattern + '\n' + stage11_addition)

# 4. Update Stage 3 - change from GitHub Pages deployment to JSON integration
stage3_old = '| **Етап 3** | Розгортання безкоштовного хостингу (GitHub Pages) — README, LICENSE, workflow | 🟡 Файли готові, потрібні облікові дані GitHub |'
stage3_new = '| **Етап 3** | Інтеграція JSON-паспортів та Google My Maps — ⏳ У процесі |'
content = content.replace(stage3_old, stage3_new)

# 5. Update Active Task
active_task_old = '**Завдання:** ✅ **Виконано (Версія 5)** — надійна валідація, Gemini-підсилення та підготовка до публікації на GitHub Pages.'
active_task_new = '**Завдання:** створення базових JSON-шаблонів regions_register.json та {region_code}_osint_passport.json.'
content = content.replace(active_task_old, active_task_new)

# 6. Add "Плани наступних цілей" section after the Active Task section
# Find the --- after Active Task and insert new section
# First, let's find where to insert - it should be after the Active Task section

# The new section content
new_goals_section = '''
## ⏭️ Плани наступних цілей, задач і робіт

1. **Реалізація Схем JSON в Excel-стилі**:
   - Створити `regions_register.json` із первинними ключами `region_code` (коди автономерів/ЗКАТО).
   - Створити шаблон OSINT-паспорта для Смотрящих Атаманів з полями для стану інфраструктури, «поганял» та оперативних сигналів.
2. **Інтеграція з Гугл Картою Імперії**:
   - Підключити карту `https://www.google.com/maps/d/u/0/edit?mid=1nVz5dLwrxEYS3dWcCXfMU2z9-6GubpE` у блок Географа/Картографа.
   - Налаштувати стикування: зчитування гео-полів із JSON-паспорта та відображення відповідних точок/шарів у картографічному інтерфейсі.
3. **Генератор Указів (`decrees.html`)**:
   - Налаштувати зчитування даних із JSON-паспорта Смотрящого Атамана для автогенерації повнотекстових указів Канцелярії.

'''

# Find the --- after Active Task section and insert before it
# Look for the pattern after Active Task
active_task_marker = '### Створені та змінені файли (Версія'
# Insert the new goals section before this marker
if active_task_marker in content:
    content = content.replace(active_task_marker, new_goals_section + active_task_marker)
else:
    # Alternative: find where to insert
    print("Could not find insertion point for goals section")

# 7. Write the updated content back
with open('c:\\kancelyariya-portal\\PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('Full update completed!')