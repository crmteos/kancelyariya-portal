# AI Context Gateway — Kancelyariya Portal

## Checkpoint 1: Schema Registry & OSINT Passports (Stage 3 Complete)
- **`chancery_manifest.json`**: Updated with `contour` fields for `worker_nodes` and formalized `osint_passport_schema` with `type`, `required`, `properties`
- **`src/data/regions_register.json`**: Created relational registry with integer `region_code` primary key (63, 77, 78)
- **`src/data/territory_passports/63_osint_passport.json`**: Created first OSINT passport for Самарська oblast conforming to formalized schema

## Checkpoint 2: Project Structure & Validation
- **`check_and_update.py`**: Enhanced with validation for regions_register.json and passport schema compliance
- **`PROJECT_STATE.md`**: Stage 3 marked complete, new files documented
- All JSON files validated: chancery_manifest.json, regions_register.json, 63_osint_passport.json

## Поточний стан проєкту (згідно з `PROJECT_STATE.md`)
- **Фаза 2** — Розробка реляційних JSON-схем даних, OSINT-паспортів та ГІС-картографії
- **Етап 3** завершено: Інтеграція JSON-паспортів та Google My Maps
- Створено файли:
  - `src/data/regions_register.json`
  - `src/data/territory_passports/63_osint_passport.json`
  - Оновлено: `chancery_manifest.json`
- Валідація: всі JSON файли пройшли синтаксичну перевірку та схвалені схемами

## Останній підсумковий звіт
### Створені файли на Етапі 3:
- `src/data/regions_register.json` — реляційний реєстр регіонів із region_code (integer) як первинний ключ
- `src/data/territory_passports/63_osint_passport.json` — OSINT-паспорт Самарського Краю (code 63) зі схемою `osint_passport_schema`
- `chancery_manifest.json` — оновлено: добавлено `contour` до worker_nodes, formalizovana schema з type/required/properties

### Оновлені файли:
- `check_and_update.py` — додана перевірка наявності regions_register.json та відповідності паспортів схемі

### Валідаційні результати:
- `chancery_manifest.json`: VALID JSON — worker_nodes have contour, schema has type/required/properties
- `regions_register.json`: VALID JSON — region_codes are integers (63, 77, 8 as int)
- `63_osint_passport.json`: VALID JSON — region_code integer, contour in allowed enum, all required fields present
- **Hotfix: GitHub Pages deployment fix** — resolved absolute fetch paths and PHP syntax errors on `index.html` line 48 by replacing `window.IMPERIAL_NEWS = <?php echo json_encode($imperial_news ?? []) ?>;` with `fetch(BASE_PATH + 'src/data/imperial_news.json')` using relative `BASE_PATH` constant, added `.then(r => { if (!r.ok) throw new Error('Failed to load imperial news') })` error guard and `try...catch` blocks with DOM fallback UI messages, added `BASE_PATH` constant in `index.html`, `admin.html`, and `decrees.html`

## Last Report
- **Task**: Remove leftover decree text and old text block from Radio section in index.html
- **Files Modified**: `index.html` — removed old leaked `<div>` container with "Завантаження operative сигналів..." text from Radio section (Module 2); preserved clean Radio block "📻 РАДІО «ОПРИЧНИК»** after Tanunah TV header; maintained `if (!tickerElem) return;` safety check
- **Validation**: `python check_and_update.py` — PASS: All JSON data files valid (regions_register.json, 63/77/78 OSINT passports)
- **Deployed**: GitHub `crmteos/kancelyariya-portal` — main branch updated with index.html Radio section cleanup
- **Status**: Radio section HTML structure clean — no raw decree code or leaked containers remaining in markup

- **Previous Task**: Clean fix: Rewrite Ticker Block in index.html
- **Previous Task**: Surgically remove raw JS code block from index.html body
- **Files Modified**: `index.html` — removed `if (!profile) return;` block through Ukrainian decree text (`1. ОЦІНКА СИТУАЦІЇ...` with `${data.infra_status}`, `${data.operational_signals}`), kept only `<div id="achtung-ticker-content" class="text-sm font-mono text-red-400">Завантаження operative сигналів...</div>` HTML container
- **Validation**: `python check_and_update.py` — PASS: All JSON data files valid (regions_register.json, 63/77/78 OSINT passports)
- **Deployed**: GitHub `crmteos/kancelyariya-portal` — main branch updated with index.html surgical cleanup
- **Status**: Media portal isolation complete — index.html strictly Tanunah videos + Achtung ticker with clean JSON data connectivity, no raw decree functions or raw JS in markup

## Зріз конфігурації `chancery_manifest.json`
```json
{
  "data_hub": "schema_registry_relational",
  "contours": [...],
  "worker_nodes": [
    {"name": "Новинарь", "role": "...", "memory": "src/data/imperial_news.json", "contour": "Tanunah"},
    {"name": "Вагон", "role": "...", "memory": "src/data/vagon_ahtungs.json", "contour": "Achtung"},
    {"name": "Архіваріус", "role": "...", "memory": "src/data/national_memory.json", "contour": "universal"},
    {"name": "Географ", "role": "...", "primary_registry": "regions_register.json", "primary_key": "region_code", "memory": "src/data/territory_passports", "contour": "universal"}
  ],
  "osint_passport_schema": {
    "type": "object",
    "required": ["region_code", "original_name", "imperial_title", "assigned_ataman", "contour", "coordinates", "osint_profile"],
    "properties": {
      "region_code": {"type": "integer"},
      "contour": {"type": "string", "enum": ["Tanunah", "Achtung", "universal"]},
      "coordinates": {"type": "object", "required": ["lat", "lng"], "properties": {"lat": {"type": "number"}, "lng": {"type": "number"}, "map_layer_id": {"type": "string"}}},
      "osint_profile": {"type": "object", "required": ["infrastructure_status", "smotryaschy_nickname", "social_tension", "operational_signals"], "properties": {...}}
    }
  },
  ...
}
`
## Зріз конфігурації `regions_register.json`
```json
{
  "regions": [
    {
      "region_code": 63,
      "name": "Самарська область",
      "imperial_title": "Самарський Край",
      "contour": "Achtung",
      "passport_path": "src/data/territory_passports/63_osint_passport.json"
    },
    {
      "region_code": 77,
      "name": "Московская область",
      "imperial_title": "Московский Povit",
      "contour": "Tanunah",
      "passport_path": "src/data/territory_passports/77_osint_passport.json"
    },
    {
      "region_code": 78,
      "name": "Невська область",
      "imperial_title": "Невський Округ",
      "contour": "universal",
      "passport_path": "src/data/territory_passports/78_osint_passport.json"
    }
  ]
}
``` 

## Зріз конфігурації `77_osint_passport.json`
```json
{
  "region_code": 77,
  "original_name": "Кировоградська область",
  "imperial_title": "Кировоградська губернія",
  "assigned_ataman": "Смотряний Атаман КIO",
  "contour": "universal",
  "coordinates": {
    "lat": 48.5,
    "lng": 32.2
  },
  "osint_profile": {
    "infrastructure_status": "partial",
    "smotryaschy_nickname": "KIO_Observer",
    "social_tension": "low",
    "operational_signals": [
      "signal_77_01",
      "signal_77_02"
    ]
  }
}
``` 

## Зріз конфігурації `78_osint_passport.json`
```json
{
  "region_code": 78,
  "original_name": "Полтавська область",
  "imperial_title": "Полтавська губернія",
  "assigned_ataman": "Смотряний Атаман ПIO",
  "contour": "universal",
  "coordinates": {
    "lat": 49.75,
    "lng": 34.53
  },
  "osint_profile": {
    "infrastructure_status": "good",
    "smotryaschy_nickname": "PIO_Observer",
    "social_tension": "medium",
    "operational_signals": [
      "signal_78_01",
      "signal_78_02",
      "signal_78_03"
    ]
  }
}
``` 

## Зріз конфігурації `fact_appropriations.json`
```json
{
  "fact_appropriations": [
    {
      "fact_id": "MK-001",
      "real_event_source": "Parade in Mukachevo",
      "timestamp": 1700000000,
      "target_region_code": 63,
      "decree_number": "DK-2024-001",
      "appropriated_narrative": "Imperial directive issued for regional development",
      "contour": "Tanunah"
    }
  ]
}
```

