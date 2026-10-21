import re

# Read the file
with open('c:\\kancelyariya-portal\\PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if the goals section exists and what it contains
if 'Плани наступніх цілей' in content or 'Плани наступних цілей' in content:
    print('Goals section found')
    # Find it
    idx = content.find('Плани наступних цілей')
    # Print surrounding context
    print('Goals section found at index:', idx)
    print(content[idx:idx+500])
else:
    print('Goals section NOT found')

# Check for the old stage 3 text
if 'Розгортання безкоштовного хостингу' in content:
    print('\nOld stage 3 found - needs updating')
else:
    print('\nOld stage 3 not found (may already be updated)')

# Check stage 1.1
if 'Етап 1.1' in content:
    print('\nStage 1.1 found')
else:
    print('\nStage 1.1 not found')

# Check active task
if 'створення базових JSON-шаблонів' in content:
    print('\nActive task updated')
else:
    print('\nActive task may need updating')