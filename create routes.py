import sqlite3
import json

# База данных
DB_PATH = "routes.db"

# Удалим старую базу, если нужно (раскомментируй при необходимости)
# import os
# if os.path.exists(DB_PATH):
#     os.remove(DB_PATH)

# Подключение
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Создание таблицы
schedule = json.dumps({
    "mon-fri": "09:00 - 18:00",
    "sat": "09:00 - 15:00",
    "sun": "выходной"
})

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "tashkent",
    "природа",
    "🏞️ Чарвак и Чимган",
    "Маршрут для любителей природы: озеро Чарвак, горы Чимган, канатка и обед у воды.",
    "Nature lovers route: Charvak lake, Chimgan mountains, cable car and lunch by the water.",
    "Tabiatni sevuvchilar uchun marshrut: Charvak ko‘li, Chimyon tog‘lari, arqon yo‘li va tushlik.",
    "https://example.com/charvak.jpg",
    "https://maps.google.com/?q=Charvak+Lake",
    schedule,
    41.6724,
    69.7690
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "tashkent",
    "природа",
    "⛰️ Амирсой",
    "Горнолыжный курорт с панорамными видами, канатной дорогой и ресторанами.",
    "Ski resort with panoramic views, cable car, and restaurants.",
    "Panoramali ko‘rinishli chang‘i kurorti, arqon yo‘li va restoranlar.",
    "https://example.com/amirsay.jpg",
    "https://maps.google.com/?q=Amirsay+Resort",
    schedule,
    41.6578,
    69.5381
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "tashkent",
    "природа",
    "🏇 Чимган",
    "Прогулки в горах, катание на лошадях, свежий воздух и природа.",
    "Mountain walks, horse riding, fresh air, and nature.",
    "Tog‘da sayr, otga minish, toza havo va tabiat.",
    "https://example.com/chimgan.jpg",
    "https://maps.google.com/?q=Chimgan+Mountains",
    schedule,
    41.5815,
    70.0320
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "samarkand",
    "история",
    "🕌 Регистан",
    "Центральная площадь Самарканда, жемчужина восточной архитектуры.",
    "The central square of Samarkand, a gem of Eastern architecture.",
    "Samarqandning markaziy maydoni, sharq me’morchiligining durdonasi.",
    "https://example.com/registan.jpg",
    "https://maps.google.com/?q=Registan+Square+Samarkand",
    schedule,
    39.6542,
    66.9597
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "samarkand",
    "история",
    "🪦 Гур-Эмир",
    "Мавзолей Амир Темура с величественным куполом.",
    "Mausoleum of Amir Temur with a majestic dome.",
    "Amir Temur maqbarasi, ulug‘vor gumbazi bilan mashhur.",
    "https://example.com/gur-emir.jpg",
    "https://maps.google.com/?q=Gur+Emir+Mausoleum",
    schedule,
    39.6488,
    66.9445
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "bukhara",
    "история",
    "🕋 Комплекс Поикалон",
    "Исторический центр Бухары: минарет, мечеть и медресе.",
    "Historical center of Bukhara: minaret, mosque, and madrasah.",
    "Buxoroning tarixiy markazi: minorasi, masjidi va madrasasi.",
    "https://example.com/poi-kalyan.jpg",
    "https://maps.google.com/?q=Poi+Kalyan+Bukhara",
    schedule,
    39.7746,
    64.4221
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "bukhara",
    "история",
    "🕍 Арк Бухары",
    "Древняя цитадель с музеями, стенами и смотровыми площадками.",
    "Ancient fortress with museums, walls and viewpoints.",
    "Qadimiy qal’a: muzeylar, devorlar va kuzatuv maydonlari bilan.",
    "https://example.com/ark.jpg",
    "https://maps.google.com/?q=Ark+of+Bukhara",
    schedule,
    39.7750,
    64.4154
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "samarkand",
    "еда",
    "🍛 Самаркандский плов",
    "Традиционный плов в Самарканде. Лучшее место – Плов Центр.",
    "Traditional pilaf in Samarkand. Best place – Plov Center.",
    "Samarqandning mashhur palovi. Eng yaxshi joy – Palov markazi.",
    "https://example.com/plov.jpg",
    "https://maps.google.com/?q=Samarkand+Plov+Center",
    schedule,
    39.6529,
    66.9720
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "samarkand",
    "еда",
    "🍢 Шашлык на Сиабском базаре",
    "Попробуйте сочный шашлык на главном базаре Самарканда.",
    "Try juicy shashlik at the main Siab Bazaar.",
    "Samarqanddagi Siab bozori – mazali shashliklar joyi.",
    "https://example.com/shashlik.jpg",
    "https://maps.google.com/?q=Siab+Bazaar+Samarkand",
    schedule,
    39.6562,
    66.9593
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "samarkand",
    "природа",
    "🌲 Улуғбекский обсерваторийный парк",
    "Тихий зеленый уголок рядом с обсерваторией Улугбека.",
    "A quiet green area near Ulugh Beg Observatory.",
    "Ulug‘bek rasadxonasi yaqinidagi sokin yashil bog‘.",
    "https://example.com/observatory_park.jpg",
    "https://maps.google.com/?q=Ulugh+Beg+Observatory",
    schedule,
    39.6670,
    66.9751
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "samarkand",
    "природа",
    "🌿 Центральный парк Самарканда",
    "Городской парк с фонтанами, аттракционами и прогулочными аллеями.",
    "City park with fountains, attractions, and walking paths.",
    "Shahar bog‘i: favvoralar, attraksionlar va sayr yo‘llari bilan.",
    "https://example.com/city_park.jpg",
    "https://maps.google.com/?q=Samarkand+Central+Park",
    schedule,
    39.6541,
    66.9582
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "bukhara",
    "еда",
    "🍲 Лагман у Ляби-Хауз",
    "Попробуйте настоящий узбекский лагман у озера Ляби-Хауз.",
    "Try authentic Uzbek lagman near Lyabi-Hauz lake.",
    "Labi-Hovuz yaqinidagi haqiqiy o‘zbek lagmani.",
    "https://example.com/lagman.jpg",
    "https://maps.google.com/?q=Lyabi+Hauz+Bukhara",
    schedule,
    39.7666,
    64.4237
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "bukhara",
    "еда",
    "🍮 Сладости востока",
    "Десерты и чай на старом базаре Бухары.",
    "Oriental sweets and tea at the old Bukhara bazaar.",
    "Sharqona shirinliklar va choy – qadimiy bozorda.",
    "https://example.com/sweets.jpg",
    "https://maps.google.com/?q=Bukhara+Old+Bazaar",
    schedule,
    39.7753,
    64.4235
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "bukhara",
    "природа",
    "🌴 Сад Саманидов",
    "Исторический парк рядом с мавзолеем Саманидов.",
    "Historical garden near the Samanid Mausoleum.",
    "Samanidlar maqbarasi yaqinidagi tarixiy bog‘.",
    "https://example.com/samanids_garden.jpg",
    "https://maps.google.com/?q=Samanid+Mausoleum",
    schedule,
    39.7745,
    64.4111
))

cursor.execute("""
INSERT INTO routes (
    city, interest, title,
    description_ru, description_en, description_uz,
    photo_url, map_url, schedule_json,
    latitude, longitude
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "bukhara",
    "природа",
    "🌺 Зеленая зона Бухары",
    "Зеленый парк в новом районе города, подходящий для прогулок.",
    "Green park in the new part of the city, great for walking.",
    "Yangi hududdagi yashil bog‘ – sayr uchun ideal joy.",
    "https://example.com/green_zone.jpg",
    "https://maps.google.com/?q=Green+Park+Bukhara",
    schedule,
    39.7782,
    64.4270
))

cursor.execute("""INSERT INTO routes (city, interest, title, description_ru, description_en, description_uz, images, map_url)
VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
(
  'Tashkent', 'history',
  'Hazrati Imam majmuasi',
  'Исторический комплекс Хазрати Имам',
  'Hazrati Imam Complex',
  'Hazrati Imom majmuasi',
  '["images/hazrati_imam.jpg"]',
  'https://maps.google.com/?q=41.3301,69.2797'
))