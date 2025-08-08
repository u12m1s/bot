import aiosqlite
import json
import logging
from pathlib import Path

DB_PATH = Path("data/routes.db")
DB_PATH.parent.mkdir(exist_ok=True)


async def init_db():
    """Инициализация базы данных"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                interest TEXT,
                title_ru TEXT,
                title_en TEXT,
                title_uz TEXT,
                description_ru TEXT,
                description_en TEXT,
                description_uz TEXT,
                images TEXT,
                map_url TEXT,
                latitude REAL,
                longitude REAL,
                schedule_json TEXT
            )
        """)
        await db.commit()
        await insert_test_data()  # Эта строка должна быть!


async def insert_test_data():
    test_routes = [
        # 1. Ташкент - Природа (Чарвак и Чимган остаются)
        {
            "city": "tashkent",
            "interest": "nature",
            "title_ru": "Ботанический сад",
            "title_en": "Botanical Garden",
            "title_uz": "Botanika bog'i",
            "description_ru": "Один из крупнейших ботанических садов в Средней Азии с коллекцией более 5000 растений.",
            "description_en": "One of the largest botanical gardens in Central Asia with over 5000 plant species.",
            "description_uz": "O'rta Osiyodagi eng katta botanika bog'laridan biri, 5000 dan ortiq o'simlik turlari.",
            "images": json.dumps(["photos/tashkent_botanical1.jpg", "photos/tashkent_botanical2.jpg"]),
            "latitude": 41.3320,
            "longitude": 69.2844
        },

        # 2. Самарканд - История
        {
            "city": "samarkand",
            "interest": "history",
            "title_ru": "Мавзолей Гур-Эмир",
            "title_en": "Gur-e-Amir Mausoleum",
            "title_uz": "Gur-i Amir maqbarasi",
            "description_ru": "Усыпальница Тамерлана и его потомков, шедевр средневековой архитектуры (XIV-XV вв.).",
            "description_en": "Tomb of Tamerlane and his descendants, masterpiece of medieval architecture (14th-15th century).",
            "description_uz": "Amir Temur va uning avlodlarining maqbarasi, o'rta asr me'morchiligi durdonasi (14-15-asrlar).",
            "images": json.dumps(["photos/gur_emir1.jpg", "photos/gur_emir2.jpg"]),
            "latitude": 39.6489,
            "longitude": 66.9687
        },

        # 3. Бухара - Культура
        {
            "city": "bukhara",
            "interest": "culture",
            "title_ru": "Театр кукол",
            "title_en": "Puppet Theater",
            "title_uz": "Qo'g'irchoq teatri",
            "description_ru": "Уникальный театр с традиционными узбекскими куклами и представлениями.",
            "description_en": "Unique theater with traditional Uzbek puppets and performances.",
            "description_uz": "An'anaviy o'zbek qo'g'irchoqlari va spektakllari bilan noyob teatr.",
            "images": json.dumps(["photos/bukhara_theater1.jpg"]),
            "latitude": 39.7755,
            "longitude": 64.4223
        },

        # 4. Хива - История
        {
            "city": "khiva",
            "interest": "history",
            "title_ru": "Ичан-Кала",
            "title_en": "Itchan Kala",
            "title_uz": "Ichan Qal'a",
            "description_ru": "Внутренний город-крепость Хивы, объект Всемирного наследия ЮНЕСКО.",
            "description_en": "Inner fortress-city of Khiva, UNESCO World Heritage Site.",
            "description_uz": "Xivaning ichki qal'asi, YuNESKOning Jahon merosi obyekti.",
            "images": json.dumps(["photos/ichan_kala1.jpg", "photos/ichan_kala2.jpg"]),
            "latitude": 41.3785,
            "longitude": 60.3620
        },

        # 5. Фергана - Шопинг
        {
            "city": "fergana",
            "interest": "shopping",
            "title_ru": "Ферганский базар",
            "title_en": "Fergana Bazaar",
            "title_uz": "Farg'ona bozori",
            "description_ru": "Яркий восточный базар с керамикой, шелками и местными деликатесами.",
            "description_en": "Vibrant oriental bazaar with ceramics, silks and local delicacies.",
            "description_uz": "Sopol buyumlar, ipak matolar va mahalliy taomlar bilan rangli sharq bozori.",
            "images": json.dumps(["photos/fergana_bazaar1.jpg"]),
            "latitude": 40.3795,
            "longitude": 71.7862
        }
        # Можно добавить еще маршруты...
    ]

    async with aiosqlite.connect(DB_PATH) as db:
        # Проверяем, есть ли уже данные
        cursor = await db.execute("SELECT COUNT(*) FROM routes")
        count = (await cursor.fetchone())[0]
        await cursor.close()

        if count == 0:
            for route in test_routes:
                await db.execute("""
                    INSERT INTO routes (
                        city, interest, title_ru, title_en, title_uz,
                        description_ru, description_en, description_uz,
                        images, latitude, longitude, schedule_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    route["city"], route["interest"],
                    route["title_ru"], route["title_en"], route["title_uz"],
                    route["description_ru"], route["description_en"], route["description_uz"],
                    route.get("images", json.dumps([])),
                    route.get("latitude", 0),
                    route.get("longitude", 0),
                    route.get("schedule_json")
                ))
            await db.commit()


async def get_routes_by_city_and_interest(city: str, interest: str, lang: str):
    """Получение маршрутов по городу и интересу"""
    if lang not in ("ru", "en", "uz"):
        lang = "ru"

    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute("""
                                    SELECT id,
                                           title_ru,
                                           title_en,
                                           title_uz,
                                           description_ru,
                                           description_en,
                                           description_uz,
                                           images,
                                           map_url,
                                           latitude,
                                           longitude,
                                           schedule_json
                                    FROM routes
                                    WHERE city = ?
                                      AND interest = ?
                                    """, (city, interest))

        rows = await cursor.fetchall()
        await cursor.close()

    routes = []
    for row in rows:
        routes.append({
            "id": row["id"],
            "title": row[f"title_{lang}"],
            "description": row[f"description_{lang}"],
            "images": json.loads(row["images"]) if row["images"] else [],
            "map_url": row["map_url"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "schedule": json.loads(row["schedule_json"]) if row["schedule_json"] else None
        })

    return routes


async def get_route_by_id(route_id: int, lang: str):
    """Получение маршрута по ID"""
    if lang not in ("ru", "en", "uz"):
        lang = "ru"

    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute("""
                                    SELECT title_ru,
                                           title_en,
                                           title_uz,
                                           description_ru,
                                           description_en,
                                           description_uz,
                                           images,
                                           map_url,
                                           latitude,
                                           longitude,
                                           schedule_json
                                    FROM routes
                                    WHERE id = ?
                                    """, (route_id,))

        row = await cursor.fetchone()
        await cursor.close()

    if not row:
        return None

    return {
        "title": row[f"title_{lang}"],
        "description": row[f"description_{lang}"],
        "images": json.loads(row["images"]) if row["images"] else [],
        "map_url": row["map_url"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "schedule": json.loads(row["schedule_json"]) if row["schedule_json"] else None
    }
