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
