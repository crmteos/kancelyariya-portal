import json
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
# Validate regions_register.json and passports
print("\n=== Validating regions_register.json and OSINT passports ===")

regions_file = "src/data/regions_register.json"
try:
    with open(regions_file, "r", encoding="utf-8") as f:
        regions_data = json.load(f)
    for region in regions_data.get("regions", []):
        if not isinstance(region.get("region_code"), int):
            print(f"ERROR: region_code must be integer for {region}")
            exit(1)
    for region in regions_data.get("regions", []):
        passport_path = region.get("passport_path", "")
        try:
            with open(passport_path, "r", encoding="utf-8") as pf:
                passport_data = json.load(pf)
            with open("chancery_manifest.json", "r", encoding="utf-8") as mf:
                manifest = json.load(mf)
            schema = manifest.get("osint_passport_schema", {})
            required = schema.get("required", [])
            properties = schema.get("properties", {})
            for field in required:
                if field not in passport_data:
                    print(f"ERROR: Missing required field \"{field}\" in {passport_path}")
                    exit(1)
            if "region_code" in properties and "type" in properties["region_code"]:
                if "region_code" in passport_data:
                    if not isinstance(passport_data["region_code"], int):
                        print(f"ERROR: region_code must be integer in {passport_path}")
                        exit(1)
            if "contour" in properties and "enum" in properties["contour"]:
                if "contour" in passport_data:
                    if passport_data["contour"] not in properties["contour"]["enum"]:
                        print(f"ERROR: contour not in allowed enum in {passport_path}")
                        exit(1)
            print(f"PASS: {passport_path} - valid schema")
        except FileNotFoundError:
            print(f"ERROR: Passport file not found: {passport_path}")
            exit(1)
except FileNotFoundError:
    print(f"ERROR: {regions_file} not found")
    exit(1)

print("Validation passed: regions_register.json and passports are valid")