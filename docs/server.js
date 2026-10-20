const express = require('express');
const path = require('path');
const { createClient } = require('@supabase/supabase-js');
const Parser = require('rss-parser');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8080;

const parser = new Parser({
  headers: { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 ImperialPortal/1.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
  },
  timeout: 7000
});

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Налаштування клієнта Supabase
const supabaseUrl = process.env.SUPABASE_URL || '';
const supabaseKey = process.env.SUPABASE_ANON_KEY || '';
let supabase = null;

if (supabaseUrl && supabaseKey && !supabaseUrl.includes('your-supabase-url')) {
  try {
    supabase = createClient(supabaseUrl, supabaseKey);
    console.log("[SUPABASE] Клієнт успішно ініціалізовано.");
  } catch (err) {
    console.error("[SUPABASE] Помилка ініціалізації клієнта:", err.message);
  }
}

// Ключ OpenRouter
const OPENROUTER_KEY = process.env.OPENROUTER_API_KEY;

// Глобальний стан аудиту
let healthStatus = {
  status: "OK",
  last_audit: new Date().toISOString(),
  quota_warnings: [],
  nodes: {
    chancellery: "GREEN",
    portal: "GREEN",
    media_empire: "GREEN",
    treasurer: "GREEN",
    novynar: "GREEN",
    vagon_doslidnykiv: "GREEN"
  }
};

// --- ВАГОН ДОСЛІДНИКІВ: СИРІ СИГНАЛИ ДЛЯ АВТО-СКАНУВАННЯ ---
const VAGON_RAW_SIGNALS = [
  { source: "yaplakal.com", text: "В Тюмени отменили половину автобусов из-за нехватки водителей, люди стоят часами на остановках в мороз -25." },
  { source: "forum_samara", text: "В Самаре опять прорвало теплотрассу, половина города без отопления, мэр уехал на курорт." },
  { source: "t.me/piter_chats", text: "Цены на бензин АИ-95 выросли на 3 рубля за неделю, на заправках начинаются споры и драки." },
  { source: "belta_internal", text: "Лукашенко посетил трикотажную фабрику и потребовал увеличить выпуск мужских носков в два раза для нужд обороны." },
  { source: "t.me/irkutsk_news", text: "В Иркутской области массовые отключения света, люди топят печи в многоквартирных домах." }
];

// --- АРХІВАРІУС: СИРІ ІСТОРИЧНІ МІФИ ДЛЯ ДЕКОНСТРУКЦІЇ ---
const ARCHIVIST_RAW_MYTHS = [
  { source: "Кремль", text: "Гоголь — великий русский писатель, основоположник реализма в русской литературе." },
  { source: "РПЦ", text: "Крещение Руси в Киеве — это начало единой великой русской православной цивилизации." },
  { source: "Минобразования РФ", text: "Основание Харькова и Одессы — это исключительно заслуга русских царей и Екатерины II." },
  { source: "Эрмитаж", text: "Илья Репин и Казимир Малевич — великие русские художники, гордость русской культуры." }
];

// Резервні локальні сховища (Fallback)
let vagonLiveAhtungs = [
  {
    id: 1,
    title: "Аномальний сплеск паніки на тему мобілізації в Тверській області",
    rawSource: "yaplakal.com (Архів Вагону)",
    rawText: "Милиция и военкомы оцепили Tver область, раздают повестки прямо в автобусах.",
    processedSatire: "Канцелярія успешно завершила зеркальный тест: Тверской военкомат переведен на прием отчетов в Клейнод-Коинах. Военком сбежал.",
    date: new Date(Date.now() - 3600000).toISOString()
  }
];

let imperialNews = [
  {
    id: 1,
    title: "Новинарь получил живой ИИ-разум на русском языке",
    originalTitle: "Запуск интеллектуальной модели",
    originalSource: "Новинарь",
    interpretation: "Отныне каждое событие анализируется и полностью переписывается уникальным стилем...",
    date: new Date().toISOString()
  }
];

let futurologyForecasts = [
  {
    id: 1,
    contour: "TANUNAH",
    region: "SAMARA",
    topic: "Енергетичний суверенітет Метрополії 2030",
    optimistic: "Повне об'єднання енергетичних систем з ЄЕС, запуск перших імперських термоядерних реакторів та експорт дешевої енергії союзникам.",
    base: "Стабільна адаптація європейських енергетичних пакетів, планова модернізація АЕС.",
    strategic: "Впровадження децентралізованих смарт-мереж по всій території Метрополії для захисту від когнітивних та фізичних загроз.",
    date: new Date().toISOString()
  }
];

let archivistChronicles = [
  {
    id: 1,
    contour: "TANUNAH",
    topic: "Гоголь — великий русский писатель",
    summary: "Реституція когнітивної спадщини Миколи Гоголя.",
    truth: "Микола Гоголь — видатний український письменник Метрополії...",
    asset: "Микола Гоголь (письменник України-Метрополії)",
    date: new Date().toISOString()
  }
];

let territoryPassports = [
  {
    id: 1,
    contour: "ACHTUNG",
    region_code: "BY-GOMEL",
    region_name: "Гомельский уезд",
    local_leaders: "Привалов (председатель горисполкома)",
    bottlenecks: "Катастрофическое состояние дорожного покрытия по улице Советской, срыв отопительного сезона.",
    decree_text: "РАСПОРЯЖЕНИЕ КАНЦЕЛЯРИИ №112-Б: Немедленно начать ремонт дорожного полотна по ул. Советской. В случае саботажа – личная административная ответственность чиновника Привалова перед Метрополией.",
    date: new Date().toISOString()
  }
];

// --- ІНТЕГРАЦІЯ З БАЗОЮ ДАНИХ (ДОВГОСТРОКОВА ПАМ'ЯТЬ З FALLBACK) ---

// 1. Новинарь
async function getImperialNews() {
  if (supabase) {
    try {
      const { data, error } = await supabase.from('imperial_news').select('*').order('id', { ascending: false }).limit(50);
      if (!error && data) {
        return data.map(item => ({
          id: item.id,
          title: item.title,
          originalTitle: item.original_title,
          originalSource: item.original_source,
          interpretation: item.interpretation,
          date: item.created_at || new Date().toISOString()
        }));
      }
    } catch (err) {
      console.error("[SUPABASE GET EXCEPTION]", err.message);
    }
  }
  return imperialNews;
}

async function saveImperialNewsItem(item) {
  const existsInMemory = imperialNews.some(existing => existing.title === item.title);
  if (!existsInMemory) imperialNews.unshift(item);

  if (supabase) {
    try {
      const { data: duplicate } = await supabase.from('imperial_news').select('id').eq('title', item.title).limit(1);
      if (!duplicate || duplicate.length === 0) {
        await supabase.from('imperial_news').insert([{
          title: item.title,
          original_title: item.originalTitle,
          original_source: item.originalSource,
          interpretation: item.interpretation
        }]);
      }
    } catch (err) {
      console.error("[SUPABASE INSERT EXCEPTION]", err.message);
    }
  }
}

// 2. Вагон Дослідників
async function getVagonAhtungs() {
  if (supabase) {
    try {
      const { data, error } = await supabase.from('vagon_ahtungs').select('*').order('id', { ascending: false }).limit(50);
      if (!error && data) {
        return data.map(item => ({
          id: item.id,
          title: item.title || "Виявлено аномалію",
          rawSource: item.raw_source,
          rawText: item.raw_text,
          processedSatire: item.processed_satire,
          date: item.created_at || new Date().toISOString()
        }));
      }
    } catch (err) {
      console.error("[SUPABASE VAGON GET EXCEPTION]", err.message);
    }
  }
  return vagonLiveAhtungs;
}

async function saveVagonAhtungItem(item) {
  const existsInMemory = vagonLiveAhtungs.some(existing => existing.rawText === item.rawText);
  if (!existsInMemory) vagonLiveAhtungs.unshift(item);

  if (supabase) {
    try {
      await supabase.from('vagon_ahtungs').insert([{
        title: item.title,
        raw_source: item.rawSource,
        raw_text: item.rawText,
        processed_satire: item.processedSatire
      }]);
    } catch (err) {
      console.error("[SUPABASE VAGON INSERT EXCEPTION]", err.message);
    }
  }
}

// 3. Футуролог
async function getFuturologyForecasts() {
  if (supabase) {
    try {
      const { data, error } = await supabase.from('futurology_forecasts').select('*').order('id', { ascending: false }).limit(50);
      if (!error && data) {
        return data.map(item => ({
          id: item.id,
          contour: item.contour,
          region: item.region || 'ALL',
          topic: item.topic,
          optimistic: item.optimistic,
          base: item.base,
          strategic: item.strategic,
          date: item.created_at || new Date().toISOString()
        }));
      }
    } catch (err) {
      console.error("[SUPABASE FUTUOLOGY GET EXCEPTION]", err.message);
    }
  }
  return futurologyForecasts;
}

async function saveFuturologyForecastItem(item) {
  const existsInMemory = futurologyForecasts.some(existing => existing.topic === item.topic && existing.contour === item.contour);
  if (!existsInMemory) futurologyForecasts.unshift(item);

  if (supabase) {
    try {
      await supabase.from('futurology_forecasts').insert([{
        contour: item.contour,
        region: item.region || 'ALL',
        topic: item.topic,
        optimistic: item.optimistic,
        base: item.base,
        strategic: item.strategic
      }]);
    } catch (err) {
      console.error("[SUPABASE FUTUROLOGY INSERT EXCEPTION]", err.message);
    }
  }
}

// 4. Архіваріус
async function getArchivistChronicles() {
  if (supabase) {
    try {
      const { data, error } = await supabase.from('archivist_chronicles').select('*').order('id', { ascending: false }).limit(50);
      if (!error && data) {
        return data.map(item => ({
          id: item.id,
          contour: item.contour,
          topic: item.topic,
          summary: item.summary,
          truth: item.truth,
          asset: item.asset,
          date: item.created_at || new Date().toISOString()
        }));
      }
    } catch (err) {
      console.error("[SUPABASE ARCHIVIST GET EXCEPTION]", err.message);
    }
  }
  return archivistChronicles;
}

async function saveArchivistChronicleItem(item) {
  const existsInMemory = archivistChronicles.some(existing => existing.topic === item.topic && existing.contour === item.contour);
  if (!existsInMemory) archivistChronicles.unshift(item);

  if (supabase) {
    try {
      await supabase.from('archivist_chronicles').insert([{
        contour: item.contour,
        topic: item.topic,
        summary: item.summary,
        truth: item.truth,
        asset: item.asset
      }]);
    } catch (err) {
      console.error("[SUPABASE ARCHIVIST INSERT EXCEPTION]", err.message);
    }
  }
}

// 5. Географ
async function getTerritoryPassports() {
  if (supabase) {
    try {
      const { data, error } = await supabase.from('territory_passports').select('*').order('id', { ascending: false }).limit(50);
      if (!error && data) {
        return data.map(item => ({
          id: item.id,
          contour: item.contour,
          region_code: item.region_code,
          region_name: item.region_name,
          local_leaders: item.local_leaders,
          bottlenecks: item.bottlenecks,
          decree_text: item.decree_text,
          date: item.created_at || new Date().toISOString()
        }));
      }
    } catch (err) {
      console.error("[SUPABASE GEOGRAPHER GET EXCEPTION]", err.message);
    }
  }
  return territoryPassports;
}

async function saveTerritoryPassportItem(item) {
  const existsInMemory = territoryPassports.some(existing => existing.region_code === item.region_code && existing.contour === item.contour);
  if (!existsInMemory) territoryPassports.unshift(item);

  if (supabase) {
    try {
      await supabase.from('territory_passports').insert([{
        contour: item.contour,
        region_code: item.region_code,
        region_name: item.region_name,
        local_leaders: item.local_leaders,
        bottlenecks: item.bottlenecks,
        decree_text: item.decree_text
      }]);
    } catch (err) {
      console.error("[SUPABASE GEOGRAPHER INSERT EXCEPTION]", err.message);
    }
  }
}


// --- ШІ-ГЕНЕРАТОР: НОВИНАРЬ ---
async function generateAiInterpretation(title, summary, sourceName) {
  if (!OPENROUTER_KEY || OPENROUTER_KEY.trim() === "" || OPENROUTER_KEY.includes("your-")) {
    return { title: `Имперский анализ: ${title}`, interpretation: `Ключ отсутствует.` };
  }

  try {
    const prompt = `Ты — уникальный имперский ньюсмейкер, острый сатирик и анал  тик Канцелярии Украинской Империи.
Твоя задача: взять оригинальную новость и полностью переписать ее в виде уникальной имперской интерпретации на русском языке.

ПРАВИЛА И ГЕОПОЛИТИЧЕСКИЕ НАРАТИВЫ:
1. СОЮЗНЫЙ ПРОСТРАНСТВО ЗАПАДА (ЕЕС/ЕС, Великобритания, Польша, Балтия, Румыния):
   - Полное партнерство, уважение и солидарность! Любая агрессивная риторика в сторону союзников строго запрещена.
2. ТЕРРИТОРИЯ БЕСПОРЯДКА (РФ и вассалы):
   - Уничтожающий интеллектуальный стеб, вскрывающий ложь пропаганды, организационное бессилие, убогость инфраструктуры (ЖКХ, унитазы) и абсурдность руководства.
3. ИСПОЛЬЗОВАНИЕ ПСЕВДОНИМОВ:
   - Путин -> Хуйло, Хуйлуша, царек недоимперии. Лавров -> Калантарян, грустный Конь. Симоньян -> Боброедка. Захарова -> пресс-алкаше. Lukashenko -> Синепалый, бульбофюрер.

Оригинальная новость:
Источник: ${sourceName}
Название: ${title}

ИМПЕРСКИЙ_ЗАГЛОВОК: [Тут заголовок]
ИМПЕРСКАЯ_ИНТЕРПРЕТАЦИЯ: [Тут текст, 2-3 предложения]`;

    const response = await axios.post("https://openrouter.ai/api/v1/chat/completions", {
      model: "google/gemini-2.5-flash", 
      messages: [{ role: "user", content: prompt }],
      max_tokens: 300
    }, {
      headers: { "Authorization": `Bearer ${OPENROUTER_KEY.trim()}`, "Content-Type": "application/json" },
      timeout: 15000
    });

    const aiText = response.data.choices[0].message.content || "";
    let finalTitle = `Имперский анализ: ${title}`;
    let finalInterpretation = "Переформатировано.";

    const lines = aiText.split('\n');
    for (const line of lines) {
      if (line.startsWith("ИМПЕРСКИЙ_ЗАГЛОВОК:")) finalTitle = line.replace("ИМПЕРСКИЙ_ЗАГЛОВОК:", "").trim();
      if (line.startsWith("ИМПЕРСКАЯ_ИНТЕРПРЕТАЦИЯ:")) finalInterpretation = line.replace("ИМПЕРСКАЯ_ИНТЕРПРЕТАЦИЯ:", "").trim();
    }

    return { title: finalTitle, interpretation: finalInterpretation };
  } catch (error) {
    return { title: `Ошибка ИИ: ${title}`, interpretation: "Не удалось." };
  }
}

// --- ШІ-ГЕНЕРАТОР: ВАГОН ДОСЛІДНИКІВ ---
async function generateVagonAhtung(rawText, rawSource) {
  if (!OPENROUTER_KEY || OPENROUTER_KEY.trim() === "" || OPENROUTER_KEY.includes("your-")) {
    return { title: `Аномалия: ${rawSource}`, processedSatire: `Ошибка ключа.` };
  }

  try {
    const prompt = `Ты — ШИ-агент "Вагон Исследователей" Канцелярии Украинской Империи.
Взять сирую паническую новость, жалобу или слух из РФ и деконструировать ее в виде оперативной сатирической сводки.

Сирая чутка:
Источник: ${rawSource}
Текст: ${rawText}

ОТЧЕТ_ЗАГОЛОВОК: [Тут заголовок]
ОТЧЕТ_СВОДКА: [Тут сводка, 2-3 предложения]`;

    const response = await axios.post("https://openrouter.ai/api/v1/chat/completions", {
      model: "google/gemini-2.5-flash", 
      messages: [{ role: "user", content: prompt }],
      max_tokens: 300
    }, {
      headers: { "Authorization": `Bearer ${OPENROUTER_KEY.trim()}`, "Content-Type": "application/json" },
      timeout: 15000
    });

    const aiText = response.data.choices[0].message.content || "";
    let finalTitle = `Выявлена аномалия: ${rawSource}`;
    let finalSatire = "Чутка обработана.";
    let hasFoundSatire = false;

    const lines = aiText.split('\n');
    for (const line of lines) {
      if (line.startsWith("ОТЧЕТ_ЗАГОЛОВОК:")) finalTitle = line.replace("ОТЧЕТ_ЗАГОЛОВОК:", "").trim();
      if (line.startsWith("ОТЧЕТ_СВОДКА:")) {
        finalSatire = line.replace("ОТЧЕТ_СВОДКА:", "").trim();
        hasFoundSatire = true;
      }
    }

    if (!hasFoundSatire && aiText.trim()) finalSatire = aiText.trim();

    return { title: finalTitle, processedSatire: finalSatire };
  } catch (error) {
    return { title: `Ошибка ИИ Вагона: ${rawSource}`, processedSatire: "Ошибка." };
  }
}

// --- ШІ-ГЕНЕРАТОР: ФУТУРОЛОГ ---
async function generateFuturologyForecast(contour, topic) {
  if (!OPENROUTER_KEY || OPENROUTER_KEY.trim() === "" || OPENROUTER_KEY.includes("your-")) {
    return { optimistic: "Ключ отсутствует.", base: "Ключ отсутствует.", strategic: "Ключ отсутствует." };
  }

  try {
    const prompt = `Ты — Главный ИИ-Прогнозист-футуролог Департамента Форсайта Украинской Империи. 
Твоя задача — построить стратегический прогноз на тему: "${topic}".

ТЫ ДОЛЖЕН СТРОГО СЛЕДОВАТЬ ВЫБРАННОМУ КОНТУРУ (CONTOUR = ${contour}):

При CONTOUR = TANUNAH:
- Язык генерации: Только Украинский. Style: Academic.

При CONTOUR = ACHTUNG:
- Язык генерации: Только Русский (в стиле Масяни-Футуролога и гротеска Владимира Сорокина).

Каждый прогноз ОБЯЗАТЕЛЬНО раздели на 3 сценария:
ОПТИМИСТИЧЕСКИЙ: [Текст]
БАЗОВЫЙ: [Текст]
СТРАТЕГИЧЕСКИЙ: [Текст]`;

    const response = await axios.post("https://openrouter.ai/api/v1/chat/completions", {
      model: "google/gemini-2.5-flash", 
      messages: [{ role: "user", content: prompt }],
      max_tokens: 800
    }, {
      headers: { "Authorization": `Bearer ${OPENROUTER_KEY.trim()}`, "Content-Type": "application/json" },
      timeout: 15000
    });

    const aiText = response.data.choices[0].message.content || "";
    let optimistic = "Не сгенерировано.";
    let base = "Не сгенерировано.";
    let strategic = "Не сгенерировано.";

    const lines = aiText.split('\n');
    for (const line of lines) {
      const cleanLine = line.trim();
      if (cleanLine.startsWith("ОПТИМИСТИЧЕСКИЙ:") || cleanLine.startsWith("ОПТИМІСТИЧНИЙ:")) {
        optimistic = cleanLine.replace(/ОПТИМИСТИЧЕСКИЙ:|ОПТИМІСТИЧНИЙ:/g, "").trim();
      }
      if (cleanLine.startsWith("БАЗОВЫЙ:") || cleanLine.startsWith("БАЗОВИЙ:")) {
        base = cleanLine.replace(/БАЗОВЫЙ:|БАЗОВИЙ:/g, "").trim();
      }
      if (cleanLine.startsWith("СТРАТЕГИЧЕСКИЙ:") || cleanLine.startsWith("СТРАТЕГІЧНИЙ:")) {
        strategic = cleanLine.replace(/СТРАТЕГИЧЕСКИЙ:|СТРАТЕГІЧНИЙ:/g, "").trim();
      }
    }

    return { optimistic, base, strategic };
  } catch (error) {
    return { optimistic: "Ошибка ИИ.", base: "Ошибка ИИ.", strategic: "Ошибка ИИ." };
  }
}

// --- ШІ-ГЕНЕРАТОР: АРХІВАРІУС ---
async function generateArchivistChronicle(contour, topic) {
  if (!OPENROUTER_KEY || OPENROUTER_KEY.trim() === "" || OPENROUTER_KEY.includes("your-")) {
    return { summary: "Ключ відсутній.", truth: "Ключ відсутній.", asset: "Ключ відсутній." };
  }

  try {
    const prompt = `Ты — Главный ИИ-Архивариус-Писарь Департамента Понятийного Суверенитета Украинской Империи. 
Твоя задача — разобрать и очистить от имперской фальши Московии историческое событие: "${topic}".

ТЫ ДОЛЖЕН СТРОГО СЛЕДОВАТЬ ВЫБРАННОМУ КОНТУРУ (CONTOUR = ${contour}):
При CONTOUR = TANUNAH: Только Украинский. Каноническое Писание.
При CONTOUR = ACHTUNG: Только Русский. Интеллектуальный стеб.

РЕЗЮМЕ_ХРОНИКИ: [Текст]
ИСТОРИЧЕСКАЯ_ПРАВДА: [Текст]
РЕСТИТУЦИОННЫЙ_АКТИВ: [Текст]`;

    const response = await axios.post("https://openrouter.ai/api/v1/chat/completions", {
      model: "google/gemini-2.5-flash", 
      messages: [{ role: "user", content: prompt }],
      max_tokens: 800
    }, {
      headers: { "Authorization": `Bearer ${OPENROUTER_KEY.trim()}`, "Content-Type": "application/json" },
      timeout: 15000
    });

    const aiText = response.data.choices[0].message.content || "";
    let summary = "Не сгенерировано.";
    let truth = "Не сгенерировано.";
    let asset = "Не сгенерировано.";
    let hasFoundTruth = false;

    const lines = aiText.split('\n');
    for (const line of lines) {
      const cleanLine = line.trim();
      if (cleanLine.startsWith("РЕЗЮМЕ_ХРОНИКИ:")) summary = cleanLine.replace("РЕЗЮМЕ_ХРОНИКИ:", "").trim();
      if (cleanLine.startsWith("ИСТОРИЧЕСКАЯ_ПРАВДА:") || cleanLine.startsWith("ІСТОРИЧНА_ПРАВДА:")) {
        truth = cleanLine.replace(/ИСТОРИЧЕСКАЯ_ПРАВДА:|ІСТОРИЧНА_ПРАВДА:/g, "").trim();
        hasFoundTruth = true;
      }
      if (cleanLine.startsWith("РЕСТИТУЦИОННЫЙ_АКТИВ:") || cleanLine.startsWith("РЕСТИТУЦІЙНИЙ_АКТИВ:")) {
        asset = cleanLine.replace(/РЕСТИТУЦИОННЫЙ_АКТИВ:|РЕСТИТУЦІЙНИЙ_АКТИВ:/g, "").trim();
      }
    }

    if (!hasFoundTruth && aiText.trim()) truth = aiText.trim();

    return { summary, truth, asset };
  } catch (error) {
    return { summary: "Помилка.", truth: "Помилка.", asset: "Помилка." };
  }
}

// --- ШІ-ГЕНЕРАТОР: ГЕОГРАФ (ДЗЕРКАЛЬНІ УКАЗИ КАНЦЕЛЯРІЇ - ОБХІД ФІЛЬТРІВ) ---
async function generateGeographerPassport(contour, regionCode, regionName) {
  if (!OPENROUTER_KEY || OPENROUTER_KEY.trim() === "" || OPENROUTER_KEY.includes("your-")) {
    return { leaders: "Помилка ключа.", bottlenecks: "Помилка ключа.", decree: "Помилка ключа." };
  }

  try {
    const prompt = `Ты — Главный ИИ-Географ и Картограф Департамента Картографии Украинской Империи.
Твоя задача — синтезировать Паспорт территории по региону "${regionName}" (код: ${regionCode}) и сгенерировать Дзеркальный Указ Канцелярии.

ТЫ ДОЛЖЕН СТРОГО СЛЕДОВАТЬ ВЫБРАННОМУ КОНТУРУ (CONTOUR = ${contour}):

При CONTOUR = TANUNAH:
- Язык: Только Украинский.
- Стиль: Геополитический, созидательный, академический.
- Дзеркальный Указ должен называться "СТР  ТЕГІЧНА ДИРЕКТИВА" про интеграцию в Intermarium и европейские коридоры. Пиши развернуто, подробно, не жалей слов.

При CONTOUR = ACHTUNG:
- Язык: Только Русский.
- Стиль: Жесткий административный приказ местному чиновнику периферрии (мэру, губернатору) с требованием немедленно решить коммунальные или дорожные проблемы под угрозой жестких административных и санкционных мер со стороны Канцелярии. Пиши развернуто, подробно, не жалей слов.

Выдавай ответ строго в формате:
ЧИНОВНИКИ: [Имена местных смотрящих/губернаторов]
БОЛЕВЫЕ_ТОЧКИ: [Список конкретных коммунальных, дорожных или финансовых дыр]
УКАЗ_КАНЦЕЛЯРИИ: [Текст Указа или Директивы]`;

    const response = await axios.post("https://openrouter.ai/api/v1/chat/completions", {
      model: "google/gemini-2.5-flash", 
      messages: [{ role: "user", content: prompt }],
      max_tokens: 1500
    }, {
      headers: { "Authorization": `Bearer ${OPENROUTER_KEY.trim()}`, "Content-Type": "application/json" },
      timeout: 15000
    });

    const aiText = response.data.choices[0].message.content || "";
    let leaders = "Не визначено.";
    let bottlenecks = "Не визначено.";
    let decree = "Не визначено.";

    const cleanText = aiText.replace(/\*\*/g, "").trim();
    const lowerText = cleanText.toLowerCase();

    // Наднадійний NLP-пошук індексів
    let leadersIdx = -1;
    const leaderKeys = ["чиновники:", "посадовці:", "керівники:", "смотрящие:", "чиновники :", "посадовці :"];
    for (const key of leaderKeys) {
      const idx = lowerText.indexOf(key);
      if (idx !== -1) { leadersIdx = idx + key.length; break; }
    }

    let bottlenecksIdx = -1;
    const bottleneckKeys = ["болевые_точки:", "болевые точки:", "больові_точки:", "больові точки:", "вразливості:", "проблемы:", "болеві_точки:", "болеві точки:"];
    for (const key of bottleneckKeys) {
      const idx = lowerText.indexOf(key);
      if (idx !== -1) { bottlenecksIdx = idx + key.length; break; }
    }

    let decreeIdx = -1;
    const decreeKeys = ["указ_канцелярии:", "указ_канцелярії:", "указ:", "стратегічна директива:", "директива:", "приказ:", "указ_канцелярии :", "директива :"];
    for (const key of decreeKeys) {
      const idx = lowerText.indexOf(key);
      if (idx !== -1) { decreeIdx = idx; break; }
    }

    // Витягуємо вміст
    if (leadersIdx !== -1) {
      let endIdx = (bottlenecksIdx !== -1 && bottlenecksIdx > leadersIdx) ? (bottlenecksIdx - 20) : ((decreeIdx !== -1 && decreeIdx > leadersIdx) ? decreeIdx : cleanText.length);
      if (endIdx < leadersIdx) endIdx = cleanText.length;
      leaders = cleanText.substring(leadersIdx, endIdx).replace(/:/g, "").trim();
    }

    if (bottlenecksIdx !== -1) {
      let endIdx = (decreeIdx !== -1 && decreeIdx > bottlenecksIdx) ? decreeIdx : cleanText.length;
      if (endIdx < bottlenecksIdx) endIdx = cleanText.length;
      bottlenecks = cleanText.substring(bottlenecksIdx, endIdx).replace(/:/g, "").trim();
    }

    if (decreeIdx !== -1) {
      const colonIdx = cleanText.indexOf(":", decreeIdx);
      if (colonIdx !== -1) {
        decree = cleanText.substring(colonIdx + 1).trim();
      } else {
        decree = cleanText.substring(decreeIdx).trim();
      }
    } else {
      decree = cleanText.trim();
    }

    if (leaders.length < 5) leaders = "Не визначено.";
    if (bottlenecks.length < 5) bottlenecks = "Не визначено.";
    if (decree.length < 5) decree = aiText.trim();

    return { leaders, bottlenecks, decree };
  } catch (error) {
    console.error("[GEOGRAPHER AI ERROR]", error.message);
    return { leaders: "Помилка.", bottlenecks: "Помилка.", decree: "Помилка." };
  }
}


// --- API МАРШРУТИ ---

// 1. Отримання Реєстру Регіонів
app.get('/api/geographer/regions', async (req, res) => {
  try {
    if (supabase) {
      const { data, error } = await supabase.from('regions_register').select('*').order('code', { ascending: true });
      if (!error && data) {
        return res.json(data);
      }
    }
  } catch (err) {
    console.error("[REGIONS GET ERROR]", err.message);
  }
  res.json([]);
});

// 2. Вагон Дослідників
app.get('/api/vagon/ahtungs', async (req, res) => {
  const reports = await getVagonAhtungs();
  res.json(reports);
});

app.post('/api/vagon/ahtungs', async (req, res) => {
  const { title, rawSource, rawText, processedSatire } = req.body;
  if (!rawText || !processedSatire) return res.status(400).json({ error: "Поля обов'язкові!" });

  const newAhtung = {
    title: title || "Виявлено аномалію",
    rawSource: rawSource || "yaplakal.com",
    rawText,
    processedSatire,
    date: new Date().toISOString()
  };

  await saveVagonAhtungItem(newAhtung);
  res.json({ success: true, item: newAhtung });
});

app.post('/api/vagon/generate', async (req, res) => {
  const { rawText, rawSource } = req.body;
  if (!rawText) return res.status(400).json({ error: "Текст обов'язковий!" });

  const processed = await generateVagonAhtung(rawText, rawSource);
  res.json({ success: true, title: processed.title, processedSatire: processed.processedSatire });
});

app.post('/api/vagon/auto-raid', async (req, res) => {
  try {
    const shuffled = [...VAGON_RAW_SIGNALS].sort(() => 0.5 - Math.random());
    const selected = shuffled.slice(0, 2);
    const generatedReports = [];

    for (const signal of selected) {
      const processed = await generateVagonAhtung(signal.text, signal.source);
      const newReport = {
        title: processed.title,
        rawSource: signal.source,
        rawText: signal.text,
        processedSatire: processed.processedSatire,
        date: new Date().toISOString()
      };
      await saveVagonAhtungItem(newReport);
      generatedReports.push(newReport);
    }
    res.json({ success: true, count: generatedReports.length, reports: generatedReports });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 3. Новинарь
app.get('/api/novynar/rss', async (req, res) => {
  const results = {};
  for (const [region, sources] of Object.entries(RSS_SOURCES)) {
    results[region] = [];
    for (const source of sources) {
      try {
        const feed = await parser.parseURL(source.url);
        const rawItems = feed.items.slice(0, 2);
        const processedItems = [];

        for (const item of rawItems) {
          const cleanTitle = item.title || "Без заголовку";
          const cleanSummary = item.contentSnippet || item.content || "";
          const processed = await generateAiInterpretation(cleanTitle, cleanSummary, source.name);

          const resultItem = {
            title: cleanTitle,
            link: item.link || "#",
            pubDate: item.pubDate || new Date().toISOString(),
            summary: cleanSummary,
            autoImperialTitle: processed.title,
            autoInterpretation: processed.interpretation
          };
          processedItems.push(resultItem);

          const newItem = {
            title: processed.title,
            originalTitle: cleanTitle,
            originalSource: source.name,
            interpretation: processed.interpretation,
            date: new Date().toISOString()
          };
          await saveImperialNewsItem(newItem);
        }

        results[region].push({ sourceName: source.name, status: "ONLINE", items: processedItems });
      } catch (error) {
        results[region].push({ sourceName: source.name, status: "OFFLINE", error: error.message });
      }
    }
  }
  res.json({ status: "success", timestamp: new Date().toISOString(), agent: "Новинарь", feeds: results });
});

app.get('/api/novynar/imperial', async (req, res) => {
  const news = await getImperialNews();
  res.json(news);
});

app.post('/api/novynar/imperial', async (req, res) => {
  const { title, originalTitle, originalSource, interpretation } = req.body;
  if (!title || !interpretation) return res.status(400).json({ error: "Поля обов'язкові!" });

  const newImperialItem = {
    title,
    originalTitle: originalTitle || "Прямой манифест",
    originalSource: originalSource || "Канцелярия",
    interpretation,
    date: new Date().toISOString()
  };

  await saveImperialNewsItem(newImperialItem);
  res.json({ success: true, item: newImperialItem });
});

// 4. Футуролог
app.get('/api/futurology/forecasts', async (req, res) => {
  const forecasts = await getFuturologyForecasts();
  res.json(forecasts);
});

app.post('/api/futurology/generate', async (req, res) => {
  const { contour, topic } = req.body;
  if (!topic || !contour) return res.status(400).json({ error: "Тема та Контур обов'язкові!" });

  const processed = await generateFuturologyForecast(contour, topic);
  res.json({ success: true, optimistic: processed.optimistic, base: processed.base, strategic: processed.strategic });
});

app.post('/api/futurology/forecasts', async (req, res) => {
  const { contour, region, topic, optimistic, base, strategic } = req.body;
  if (!topic || !optimistic || !base || !strategic) return res.status(400).json({ error: "Всі поля обов'язкові!" });

  const newForecast = {
    contour,
    region: region || 'ALL',
    topic,
    optimistic,
    base,
    strategic,
    date: new Date().toISOString()
  };

  await saveFuturologyForecastItem(newForecast);
  res.json({ success: true, item: newForecast });
});

// 5. Архів Хронік
app.get('/api/archivist/chronicles', async (req, res) => {
  const chronicles = await getArchivistChronicles();
  res.json(chronicles);
});

app.post('/api/archivist/generate', async (req, res) => {
  const { contour, topic } = req.body;
  if (!topic || !contour) return res.status(400).json({ error: "Тема та Контур обов'язкові!" });

  const processed = await generateArchivistChronicle(contour, topic);
  res.json({ success: true, summary: processed.summary, truth: processed.truth, asset: processed.asset });
});

app.post('/api/archivist/chronicles', async (req, res) => {
  const { contour, topic, summary, truth, asset } = req.body;
  if (!topic || !summary || !truth || !asset) return res.status(400).json({ error: "Всі поля обов'язкові!" });

  const newChronicle = {
    contour,
    topic,
    summary,
    truth,
    asset,
    date: new Date().toISOString()
  };

  await saveArchivistChronicleItem(newChronicle);
  res.json({ success: true, item: newChronicle });
});

// 6. МАРШРУТИ ГЕОГРАФА
app.get('/api/geographer/passports', async (req, res) => {
  const passports = await getTerritoryPassports();
  res.json(passports);
});

app.post('/api/geographer/generate', async (req, res) => {
  const { contour, regionCode, regionName } = req.body;
  if (!regionCode || !contour || !regionName) return res.status(400).json({ error: "Параметри обов'язкові!" });

  const processed = await generateGeographerPassport(contour, regionCode, regionName);
  res.json({ success: true, leaders: processed.leaders, bottlenecks: processed.bottlenecks, decree_text: processed.decree });
});

app.post('/api/geographer/passports', async (req, res) => {
  const { contour, regionCode, regionName, localLeaders, bottlenecks, decreeText } = req.body;
  if (!regionCode || !regionName || !localLeaders || !bottlenecks || !decreeText) {
    return res.status(400).json({ error: "Всі поля обов'язкові!" });
  }

  const newPassport = {
    contour,
    region_code: regionCode,
    region_name: regionName,
    local_leaders: localLeaders,
    bottlenecks,
    decree_text: decreeText,
    date: new Date().toISOString()
  };

  await saveTerritoryPassportItem(newPassport);
  res.json({ success: true, item: newPassport });
});


// --- 👑 АВТОНОМНИЙ ІМПЕРСЬКИЙ ОРКЕСТРАТОР (BACKGROUND AUTO-SYNC) ---

async function runOrchestraTick() {
  console.log("[ОРКЕСТР] Системний імпульс синхронізації ШІ...");
  try {
    // 1. Автоматичний запуск Вагону Дослідників (Ахтунг розвідка)
    const shuffled = [...VAGON_RAW_SIGNALS].sort(() => 0.5 - Math.random());
    const signal = shuffled[0];
    const processedVagon = await generateVagonAhtung(signal.text, signal.source);
    
    const vagonItem = {
      title: processedVagon.title,
      rawSource: signal.source,
      rawText: signal.text,
      processedSatire: processedVagon.processedSatire,
      date: new Date().toISOString()
    };
    await saveVagonAhtungItem(vagonItem);

    // 2. Автоматичний запуск Футуролога на базі отриманої розвідки!
    const randomContour = Math.random() > 0.5 ? 'TANUNAH' : 'ACHTUNG';
    const randomRegion = Math.random() > 0.5 ? '63' : '69';
    const futurologyTopic = `Аналіз когнітивного резонансу навколо події: ${processedVagon.title}`;

    console.log(`[ОРКЕСТР] Авто-прогноз на тему: ${futurologyTopic} [${randomContour}]`);
    const processedFuturologist = await generateFuturologyForecast(randomContour, futurologyTopic);
    
    await saveFuturologyForecastItem({
      contour: randomContour,
      region: randomRegion,
      topic: futurologyTopic,
      optimistic: processedFuturologist.optimistic,
      base: processedFuturologist.base,
      strategic: processedFuturologist.strategic
    });

    // 3. Автоматичний запуск Архіваріуса (деконструкція міфу)
    const shuffledMyths = [...ARCHIVIST_RAW_MYTHS].sort(() => 0.5 - Math.random());
    const selectedMyth = shuffledMyths[0];
    const mythContour = Math.random() > 0.5 ? 'TANUNAH' : 'ACHTUNG';

    console.log(`[ОРКЕСТР] Авто-деконструкція міфу: ${selectedMyth.text} [${mythContour}]`);
    const processedArchivist = await generateArchivistChronicle(mythContour, selectedMyth.text);

    await saveArchivistChronicleItem({
      contour: mythContour,
      topic: selectedMyth.text,
      summary: processedArchivist.summary,
      truth: processedArchivist.truth,
      asset: processedArchivist.asset
    });

    // 4. Автоматичний запуск Географа (Синтез паспорту та випуск Дзеркального Указу!)
    const regions = [
      { code: "63", name: "Самарский край" },
      { code: "69", name: "Тверской край" },
      { code: "32", name: "Брянский край" },
      { code: "77", name: "Масквабадский анклав" },
      { code: "BY-GOMEL", name: "Гомельский уезд" }
    ];
    const targetRegion = regions[Math.floor(Math.random() * regions.length)];
    const geographerContour = Math.random() > 0.5 ? 'TANUNAH' : 'ACHTUNG';

    console.log(`[ОРКЕСТР] Авто-паспорт Географа для: ${targetRegion.name} [${geographerContour}]`);
    const processedGeographer = await generateGeographerPassport(geographerContour, targetRegion.code, targetRegion.name);

    await saveTerritoryPassportItem({
      contour: geographerContour,
      region_code: targetRegion.code,
      region_name: targetRegion.name,
      local_leaders: processedGeographer.leaders,
      bottlenecks: processedGeographer.bottlenecks,
      decree_text: processedGeographer.decree
    });

    console.log("[ОРКЕСТР] Системний імпульс успішно завершено.");
    return { 
      success: true, 
      vagon: vagonItem, 
      futurologist_topic: futurologyTopic,
      archivist_topic: selectedMyth.text,
      geographer_region: targetRegion.name,
      contour: randomContour 
    };
  } catch (err) {
    console.error("[ОРКЕСТР ERROR]", err.message);
    return { success: false, error: err.message };
  }
}

// Запуск фонового процесу кожні 10 хвилин
setInterval(runOrchestraTick, 10 * 60 * 1000);

// Секретний ручний маршрут для миттєвого тесту Оркестру
app.get('/api/orchestra/tick', async (req, res) => {
  const result = await runOrchestraTick();
  res.json(result);
});


// Стандартні API
app.get('/api/balance', async (req, res) => {
  res.json({ fiat_balance_uah: 14500.00, crypto_balance_kln: 382.40, serfs_count: 2, land_plots: 1, is_demo: true });
});

app.get('/api/health-audit', (req, res) => {
  res.json(healthStatus);
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Медійний портал Української імперії успішно запущено на порту ${PORT}`);
});