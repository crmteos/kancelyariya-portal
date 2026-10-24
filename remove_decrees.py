with open('c:\\\\kancelyariya-portal\\\\index.html', 'r', encoding='utf8') as f:
    content = f.read()

# Remove generateTanunahTemplate function and its comment header
old1 = """// 2. ОФЛАЙН-ШАБЛОМ: TANUNAH (Стратегічна директива)
function generateTanunahTemplate(data) {
  const dateStr = new Date().toLocaleDateString('uk-UA');
  return `🏛️ СТРАТЕГІЧНА ДИРЕКТИВА КАНЦЕЛЯРІЇ №${data.number || '01/2026'}\r
`;
"""

# Remove generateAchtungTemplate function and its comment header
old2 = """// 3. ОФЛАЙН-ШАБЛОМ: ACHTUNG (Дзеркальний указ)
function generateAchtungTemplate(data) {
  const dateStr = new Date().toLocaleDateString('uk-UA');
  return `⚠️ ДЗЕРКАЛЬНИЙ УКАЗ КАНЦЕЛЯРІЇ №${data.number || '666/A'}\r
`;
"""

if old1 in content:
    content = content.replace(old1, '')
    print('Removed generateTanunahTemplate')

if old2 in content:
    content = content.replace(old2, '')
    print('Removed generateAchtungTemplate')

with open('c:\\\\kancelyariya-portal\\\\index.html', 'w', encoding='utf8') as f:
    f.write(content)

print('Done! Functions removed from index.html')