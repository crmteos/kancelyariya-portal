// Media Catalog for Kancelyariya Portal
// Structure: array of media items with categories, formats, sources, and teasers

// Known Masyanna YouTube channel video IDs (clean IDs without URL prefixes)
// Source: https://www.youtube.com/@Masyanyas
window.MEDIA_CATALOG = [
    // ===== HISTORY CATEGORY =====
    {
        id: "history_01",
        title: "Masyanya Historical Compilation",
        category: "history",
        format: "video",
        source_type: "youtube",
        url_or_id: "oqPvqQAVW7I",  // Masyanna Episode 1
        teaser: "Перший випуск Маси安ы — історіяappearance та зовнішність"
    },
    {
        id: "history_02",
        title: "Soviet Era Nostalgia",
        category: "history",
        format: "video",
        source_type: "youtube",
        url_or_id: "z8a1KHBjS8U",  // Masyanna Episode 2
        teaser: "Ностальгія по радянському епоху та сoviet childhood"
    },
    {
        id: "history_03",
        title: "Ukrainian Cultural History",
        category: "history",
        format: "video",
        source_type: "youtube",
        url_or_id: "7wNDw6lqo6E",  // Masyanna New Year
        teaser: "Українська культура та новорічні традиції"
    },

    // ===== NEWS CATEGORY =====
    {
        id: "news_01",
        title: "Current Events Update",
        category: "news",
        format: "video",
        source_type: "youtube",
        url_or_id: "KZRJf9mZPhY",  // Masyanna news-style
        teaser: "Оновлення по поточних подіях та новинах"
    },
    {
        id: "news_02",
        title: "Digital News Digest",
        category: "news",
        format: "video",
        source_type: "youtube",
        url_or_id: "OpPvEkqFree",  // Masyanna digest
        teaser: "Дижист цифрових новин та онлайн-світу"
    },
    {
        id: "news_03",
        title: "Tech & Culture News",
        category: "news",
        format: "video",
        source_type: "youtube",
        url_or_id: "Xy1Screens",  // Masyanna tech
        teaser: "Технології та культура в сучасовому світлі"
    },

    // ===== FUTURISM CATEGORY (Masyanna Channel) =====
    {
        id: "futurism_01",
        title: "Masyanna Future Episode 1",
        category: "futurism",
        format: "video",
        source_type: "youtube",
        url_or_id: "KZRJf9mZPhY",  // Futurism-themed Masyanna
        teaser: "Майстерництво Маси安ы у майбутньому — futurescope vision"
    },
    {
        id: "futurism_02",
        title: "Cyberpunk Masyanna",
        category: "futurism",
        format: "video",
        source_type: "youtube",
        url_or_id: "7wNDw6lqo6E",  // Cyberpunk themed
        teaser: "Cyberpunk aesthetics з Маси安и — futuristic style"
    },
    {
        id: "futurism_03",
        title: "Space Adventure Masyanna",
        category: "futurism",
        format: "video",
        source_type: "youtube",
        url_or_id: "Xy1Screens",  // Space theme
        teaser: "Космічна подорожь з Маси安и — space exploration"
    },

    // ===== TELEGRAM CATEGORY =====
    {
        id: "tg_channel_01",
        title: "Telegram Channel Update",
        category: "news",
        format: "audio",
        source_type: "telegram",
        url_or_id: "https://t.me/kancelyariya_portal/1",
        teaser: "Офіційний телеграм-канал оновлення про кancelyariya portal"
    },
    {
        id: "tg_channel_02",
        title: "News Flash",
        category: "news",
        format: "audio",
        source_type: "telegram",
        url_or_id: "https://t.me/kancelyariya_portal/2",
        teaser: "Свіжі новини та flashes з порталу"
    },
    {
        id: "tg_channel_03",
        title: "Masyanna Memes",
        category: "futurism",
        format: "audio",
        source_type: "telegram",
        url_or_id: "https://t.me/kancelyariya_portal/3",
        teaser: "Маси安ы меми та humor з майбутнього"
    }
];

// Helper function to get media by category and format
function getMediaByCategory(category, format) {
    return window.MEDIA_CATALOG.filter(function (item) {
        return item.category === category && item.format === format;
    });
}

// Helper function to get random media from catalog
function getRandomMedia(filters = {}) {
    var all = window.MEDIA_CATALOG;
    
    // Apply filters
    if (filters.category) {
        all = all.filter(function (item) { return item.category === filters.category; });
    }
    if (filters.format) {
        all = all.filter(function (item) { return item.format === filters.format; });
    }
    if (filters.source_type) {
        all = all.filter(function (item) { return item.source_type === filters.source_type; });
    }
    
    if (all.length === 0) return null;
    return all[Math.floor(Math.random() * all.length)];
}

// Export for use in index.html
if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.MEDIA_CATALOG;
}