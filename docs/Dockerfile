# Використовуємо офіційний стабільний образ Node.js v22
FROM node:22-slim

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо package.json та package-lock.json (якщо є)
COPY package*.json ./

# Встановлюємо залежності (включаючи наш новий rss-parser)
RUN npm install --production

# Копіюємо весь інший код проекту (server.js, публічну папку тощо)
COPY . .

# Відкриваємо порт 8080 (стандарт для Cloud Run)
EXPOSE 8080

# Запускаємо сервер
CMD ["node", "server.js"]
