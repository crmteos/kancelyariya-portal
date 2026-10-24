lines = open(r"c:\kancelyariya-portal\index.html", "r", encoding="utf-8").readlines()
open(r"c:\kancelyariya-portal\index.html", "w", encoding="utf-8").writelines(l for i, l in enumerate(lines, 1) if i < 62 or i > 99)
print("Lines 62-99 removed")