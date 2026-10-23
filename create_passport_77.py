import json

# Create the 77 OSINT passport based on the schema from chancery_manifest.json
passport = {
    "region_code": 77,
    "original_name": "Кіровоградська область",
    "imperial_title": "Кіровоградська губернія",
    "assigned_ataman": "Смотряний Атаман КIO",
    "contour": "universal",
    "coordinates": {
        "lat": 48.5,
        "lng": 32.2,
        "map_layer_id": "77kio-layer"
    },
    "osint_profile": {
        "infrastructure_status": "partial",
        "smotryaschy_nickname": "KIO_Observer",
        "social_tension": "low",
        "operational_signals": ["signal_77_01", "signal_77_02"]
    }
}

# Write the passport
with open("src/data/territory_passports/77_osint_passport.json", "w", encoding="utf-8") as f:
    json.dump(passport, f, indent=2, ensure_ascii=False)

print("Created 77_osint_passport.json")