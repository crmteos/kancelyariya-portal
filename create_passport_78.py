import json

# Create the 78 OSINT passport based on the schema from chancery_manifest.json
passport = {
    "region_code": 78,
    "original_name": "Полтавська область",
    "imperial_title": "Полтавська губернія",
    "assigned_ataman": "Смотряний Атаман ПIO",
    "contour": "universal",
    "coordinates": {
        "lat": 49.75,
        "lng": 34.53,
        "map_layer_id": "78pio-layer"
    },
    "osint_profile": {
        "infrastructure_status": "good",
        "smotryaschy_nickname": "PIO_Observer",
        "social_tension": "medium",
        "operational_signals": ["signal_78_01", "signal_78_02", "signal_78_03"]
    }
}

# Write the passport
with open("src/data/territory_passports/78_osint_passport.json", "w", encoding="utf-8") as f:
    json.dump(passport, f, indent=2, ensure_ascii=False)

print("Created 78_osint_passport.json")