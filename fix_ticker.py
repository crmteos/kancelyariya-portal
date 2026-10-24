import re

with open(r"c:\kancelyariya-portal\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the Achtung Ticker section from <!-- comment to </section>
pattern = r'<!-- Achtung Ticker: .{0,80} .{0,80} -->\n<section class="mt-6 .{0,300}</section>'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open(r"c:\kancelyariya-portal\index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done - HTML section removed")