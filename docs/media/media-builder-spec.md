# Специфікація Конструктора: Медіа-Вузли
**Призначення:** Технічні інструкції для створення, реєстрації та моніторингу вузлів Медіаімперії

🗄️ 1. Структура Бази Даних (Database Schema)
Для реєстрації вузлів конструктор має створити таблицю `media_nodes` (в Supabase чи локальній SQLite):
```sql
CREATE TABLE IF NOT EXISTS media_nodes (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL, -- telegram, viber, stream, treasurer
    status VARCHAR(20) DEFAULT "offline", -- active, offline
    last_ping TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    config TEXT -- JSON для збереження токенів чи лінків
);
```

🔌 2. API Ендпоінти у server.js
Конструктор має додати два прості маршрути у наш файл `server.js` для взаємодії з вузлами:
1. **Реєстрація/Пінг вузла (`POST /api/nodes/ping`):
   - Вузол шле свій `id`, `name`, `type` та статус.
   - Сервер оновлює запис у БД і ставить поточний час `last_ping`.
2. **Статус усіх вузлів (`GET /api/nodes`):
   - Повертає список усіх зареєстрованих вузлів та їхній стан для відображення на UI Порталу.

⚙️ 3. Бойлерплейт Вузла (Приклад коду реєстрації на Node.js)
Кожен новий вузол (наприклад, Телеграм-Бот) при запуску виконує цей простий запит до нашого Порталу:
```javascript
const registerNode = async () => {
  try {
    const response = await fetch("http://localhost:3000/api/nodes/ping", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: "telegram-voice-01",
        name: "Телеграм-Голос",
        type: "telegram",
        status: "active",
        config: JSON.stringify({ channel: "@imperium_news" })
      })
    });
    console.log("Вузол успішно зареєстровано.");
  } catch (err) {
    console.error("Помилка підключення до Порталу:", err.message);
  }
};
registerNode();
```

🎯 4. Покроковий План Дій для Конструктора:
- [ ] Крок 1: Створити таблицю `media_nodes` за схемою.
- [ ] Крок 2: Додати API маршрути ping/get у `server.js`.
- [ ] Крок 3: Написати простий тестовий скрипт вузла і запустити його для перевірки реєстрації.
- [ ] Крок 4: Вивести статус вузлів на головну сторінку Порталу (UI).
