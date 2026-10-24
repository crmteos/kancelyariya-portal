lines = open(r"c:\kancelyariya-portal\index.html", "r", encoding="utf-8").readlines()
open(r"c:\kancelyariya-portal\index.html", "w", encoding="utf-8").writelines(l for i, l in enumerate(lines, 1) if i < 90 or i > 101)
print("Lines 90-101 removed")