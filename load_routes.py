import sqlite3
import json

conn = sqlite3.connect("routes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    interest TEXT,
    title TEXT,
    description_ru TEXT,
    description_en TEXT,
    description_uz TEXT,
    images TEXT,
    map_url TEXT,
    latitude REAL,
    longitude REAL
)
""")

cursor.execute("DELETE FROM routes")  # Очищаем перед заполнением

routes_data = [
    {
        "city": "tashkent",
        "interest": "природа",
        "title": "🏞️ Чарвак и Чимган",
        "description_ru": "Озеро Чарвак, горы Чимган, канатка и обед у воды.",
        "description_en": "Charvak lake, Chimgan mountains, cable car and lunch by the water.",
        "description_uz": "Charvak ko‘li, Chimyon tog‘lari, arqon yo‘li va tushlik.",
        "images": json.dumps(["photos/charvak1.jpg", "photos/charvak2.jpg"]),
        "map_url": "https://maps.google.com/?q=Charvak+Lake",
        "latitude": 41.6724,
        "longitude": 69.7690
    },
    {
        "city": "samarkand",
        "interest": "история",
        "title": "🏛 Регистан",
        "description_ru": "Знаменитая площадь с медресе XIV века в Самарканде.",
        "description_en": "Famous square with 14th-century madrasahs in Samarkand.",
        "description_uz": "Samarqanddagi XIV asr madrasalari bilan mashhur maydon.",
        "images": json.dumps(["photos/registan1.jpg"]),
        "map_url": "https://maps.google.com/?q=Registan+Samarkand",
        "latitude": 39.6542,
        "longitude": 66.9597
    },
    {
        "city": "samarkand",
        "interest": "еда",
        "title": "🍽️ Самаркандская пловная",
        "description_ru": "Настоящий узбекский плов в старом городе.",
        "description_en": "Real Uzbek plov in the old town.",
        "description_uz": "Eski shaharda haqiqiy o‘zbek palovi.",
        "images": json.dumps(["photos/plov_samarkand.jpg"]),
        "map_url": "https://maps.google.com/?q=Plov+Center+Samarkand",
        "latitude": 39.6590,
        "longitude": 66.9750
    },
    {
        "city": "bukhara",
        "interest": "еда",
        "title": "🍽️ Ляби-Хауз",
        "description_ru": "Национальная кухня у водоема в сердце Бухары.",
        "description_en": "National cuisine near the pond in the heart of Bukhara.",
        "description_uz": "Buxoro markazidagi hovuz yonida milliy taomlar.",
        "images": json.dumps(["photos/lyabi1.jpg"]),
        "map_url": "https://maps.google.com/?q=Lyabi+Khauz+Bukhara",
        "latitude": 39.7745,
        "longitude": 64.4282
    },
    {
        "city": "bukhara",
        "interest": "природа",
        "title": "🌿 Ситораи Мохи Хоса",
        "description_ru": "Загородная резиденция эмира с прекрасным садом.",
        "description_en": "Country residence of the Emir with a beautiful garden.",
        "description_uz": "Amirning go‘zal bog‘li qishloq qarorgohi.",
        "images": json.dumps(["photos/sitorai1.jpg"]),
        "map_url": "https://maps.google.com/?q=Sitorai+Mokhi-Khosa+Bukhara",
        "latitude": 39.8031,
        "longitude": 64.4682
    }
]

for route in routes_data:
    cursor.execute("""
        INSERT INTO routes (
            city, interest, title,
            description_ru, description_en, description_uz,
            images, map_url, latitude, longitude
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        route["city"],
        route["interest"],
        route["title"],
        route["description_ru"],
        route["description_en"],
        route["description_uz"],
        route["images"],
        route["map_url"],
        route["latitude"],
        route["longitude"]
    ))

conn.commit()
conn.close()
print("✅ Готово! Данные загружены.")
