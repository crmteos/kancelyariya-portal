import json

with open("src/data/kleyrody_insignia.json", "r", encoding="utf-8") as f:
    insignia = json.load(f)

with open("chancery_manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

with open("src/data/kernel_telemetry.json", "r", encoding="utf-8") as f:
    telemetry = json.load(f)

with open("src/data/fact_appropriations.json", "r", encoding="utf-8") as f:
    facts = json.load(f)

print("Data files loaded successfully")
print("Insignia nodes:", list(insignia["insignia_matrix"]["nodes"].keys()))
print("Manifest related_schemas:", list(manifest["related_schemas"].keys()))
print("Telemetry:", telemetry)
print("Facts:", facts["fact_appropriations"])