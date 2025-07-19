DROP TABLE IF EXISTS routes;

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

-- Tashkent — Природа
INSERT INTO routes (
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
        {"time": "09:00", "activity_ru": "Поездка к озеру", "activity_en": "Trip to the lake", "activity_uz": "Ko‘lga sayohat"},
        {"time": "11:00", "activity_ru": "Катание на канатке", "activity_en": "Cable car ride", "activity_uz": "Arqon yo‘lida sayr"},
        {"time": "13:00", "activity_ru": "Обед у воды", "activity_en": "Lunch near water", "activity_uz": "Suv bo‘yida tushlik"}
    ]'
);

-- Tashkent — Еда
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json
) VALUES (
    'tashkent',
    'еда',
    '🍽️ Гастро-тур по Ташкенту',
    'Попробуйте плов в центре, чучвару в Чигатае и чай с лепёшкой в чайхане.',
    'Try plov in the city center, chuchvara in Chigatay and tea with bread in a chaikhana.',
    'Toshkent markazida palov, Chig‘atoyda chuchvara va choyxona noni bilan choy.',
    'https://example.com/food.jpg',
    'https://maps.google.com/?q=Plov+Center+Tashkent',
    '[
        {"time": "10:00", "activity_ru": "Завтрак в чайхане", "activity_en": "Breakfast in chaikhana", "activity_uz": "Choyxonada nonushta"},
        {"time": "12:00", "activity_ru": "Плов-центр", "activity_en": "Plov Center", "activity_uz": "Palov markazi"},
        {"time": "14:00", "activity_ru": "Чучвара в Чигатае", "activity_en": "Chuchvara in Chigatay", "activity_uz": "Chig‘atoyda chuchvara"},
        {"time": "16:00", "activity_ru": "Десерт в кафе", "activity_en": "Dessert at cafe", "activity_uz": "Kafeda desert"}
    ]'
);

-- Samarkand — История
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json
) VALUES (
    'samarkand',
    'история',
    '🏛️ Регистан',
    'Знаменитая площадь с тремя великолепными медресе.',
    'Famous square with three majestic madrasahs.',
    'Uchta ulug‘vor madrasali mashhur maydon.',
    'https://example.com/registan.jpg',
    'https://maps.google.com/?q=Registan',
    '{
        "08:30": "Встреча с гидом у отеля",
        "09:00": "Экскурсия по площади Регистан",
        "11:00": "Посещение медресе Улугбека",
        "12:30": "Свободное время"
    }'
);

-- Bukhara — История
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json
) VALUES (
    'bukhara',
    'история',
    '🏰 Цитадель Арк и Ляби-Хауз',
    'Исторический маршрут: крепость Арк, ансамбль Ляби-Хауз, прогулка по древним улицам.',
    'Historical route: Ark Fortress, Lyabi-Hauz complex, walk through ancient streets.',
    'Tarixiy marshrut: Ark qal’asi, Labi Hovuz majmuasi, qadimiy ko‘chalarda sayr.',
    'https://example.com/ark.jpg',
    'https://maps.google.com/?q=Ark+Fortress+Bukhara',
    '[
        {"time": "10:00", "activity_ru": "Цитадель Арк", "activity_en": "Ark Fortress", "activity_uz": "Ark qal’asi"},
        {"time": "12:00", "activity_ru": "Ляби-Хауз", "activity_en": "Lyabi-Hauz", "activity_uz": "Labi Hovuz"},
        {"time": "14:00", "activity_ru": "Посещение рынка", "activity_en": "Visit to local bazaar", "activity_uz": "Bozorga tashrif"},
        {"time": "16:00", "activity_ru": "Старый город", "activity_en": "Old city walk", "activity_uz": "Eski shahar bo‘ylab sayr"}
    ]'
);
