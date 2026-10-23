import os
d = "src/data/territory_passports"
if os.path.exists(d):
    files = os.listdir(d)
    print(files)
else:
    print("not found")