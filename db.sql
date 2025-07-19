CREATE TABLE routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    interest TEXT NOT NULL,
    title TEXT NOT NULL,
    description_ru TEXT,
    description_en TEXT,
    description_uz TEXT,
    photo_url TEXT,
    map_url TEXT,
    schedule_json TEXT
);

INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json
)INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json
) VALUES (
    'tashkent',
    'природа',
    '🏞️ Чарвак и Чимган',
    'Маршрут для любителей природы: озеро Чарвак, горы Чимган, канатка и обед у воды.',
    'Nature lovers route: Charvak lake, Chimgan mountains, cable car and lunch by the water.',
    'Tabiatni sevuvchilar uchun marshrut: Charvak ko‘li, Chimyon tog‘lari, arqon yo‘li va tushlik.',
    'https://example.com/charvak.jpg',
    'https://maps.google.com/?q=Charvak+Lake',
    '[
        {"time": "09:00", "activity_ru": "Выезд", "activity_en": "Departure", "activity_uz": "Jo‘nab ketish"},
        {"time": "11:00", "activity_ru": "Озеро Чарвак", "activity_en": "Charvak Lake", "activity_uz": "Charvak ko‘li"},
        {"time": "13:00", "activity_ru": "Обед", "activity_en": "Lunch", "activity_uz": "Tushlik"},
        {"time": "15:00", "activity_ru": "Канатная дорога", "activity_en": "Cable car", "activity_uz": "Arqon yo‘li"},
        {"time": "18:00", "activity_ru": "Возвращение", "activity_en": "Return", "activity_uz": "Qaytish"}
    ]'
);


