import json

# Validate chancery_manifest.json
with open('chancery_manifest.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
print('chancery_manifest.json: VALID JSON')
print('Worker nodes:')
for n in d['worker_nodes']:
    print('  ' + n['name'] + ': contour=' + n.get('contour', 'MISSING'))

# Validate regions_register.json
with open('src/data/regions_register.json', 'r', encoding='utf-8') as f:
    r = json.load(f)
print('regions_register.json: VALID JSON')
for reg in r['regions']:
    print('  region_code=' + str(reg['region_code']) + ' (' + type(reg['region_code']).__name__ + ') ' + reg['name'])

# Validate 63 passport
with open('src/data/territory_passports/63_osint_passport.json', 'r', encoding='utf-8') as f:
    p = json.load(f)
print('63_osint_passport.json: VALID JSON')
print('  region_code=' + str(p['region_code']) + ' (' + type(p['region_code']).__name__ + ')')
print('  contour=' + p['contour'])
required = ['region_code', 'original_name', 'imperial_title', 'assigned_ataman', 'contour', 'coordinates', 'osint_profile']
print('  All required fields present: ' + str(all(f in p for f in required)))
print('  region_code is integer: ' + str(isinstance(p['region_code'], int)))
print('  contour in allowed enum: ' + str(p['contour'] in ['Tanunah', 'Achtung', 'universal']))