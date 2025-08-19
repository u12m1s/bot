# db.py — PostgreSQL / asyncpg
import os
import json
import asyncpg
from typing import Optional

POOL: Optional[asyncpg.Pool] = None
DATABASE_URL = os.getenv("DATABASE_URL")  # Render / внешняя БД дадут одну строку подключения

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS routes (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    interest TEXT NOT NULL,
    title_ru TEXT NOT NULL,
    title_en TEXT NOT NULL,
    title_uz TEXT NOT NULL,
    description_ru TEXT NOT NULL,
    description_en TEXT NOT NULL,
    description_uz TEXT NOT NULL,
    images JSONB DEFAULT '[]'::jsonb,
    map_url TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    schedule_json JSONB
);
CREATE INDEX IF NOT EXISTS idx_routes_city_interest ON routes (city, interest);
"""

TEST_DATA = [
    {
        "city": "tashkent",
        "interest": "nature",
        "title_ru": "Ботанический сад",
        "title_en": "Botanical Garden",
        "title_uz": "Botanika bog'i",
        "description_ru": "Один из крупнейших ботанических садов в Средней Азии с коллекцией более 5000 растений.",
        "description_en": "One of the largest botanical gardens in Central Asia with over 5000 plant species.",
        "description_uz": "O'rta Osiyodagi eng katta botanika bog'laridan biri, 5000 dan ortiq o'simlik turlari.",
        "images": ["photos/tashkent_botanical1.jpg", "photos/tashkent_botanical2.jpg"],
        "map_url": None,
        "latitude": 41.3320,
        "longitude": 69.2844,
        "schedule_json": None
    }
]

async def init_db():
    """Создаёт пул, схему и, если таблица пуста, — тестовые данные."""
    global POOL
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")

    if POOL is None:
        POOL = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)

    async with POOL.acquire() as conn:
        await conn.execute(SCHEMA_SQL)
        count = await conn.fetchval("SELECT COUNT(*) FROM routes;")
        if count == 0:
            insert_sql = """
            INSERT INTO routes (
                city, interest, title_ru, title_en, title_uz,
                description_ru, description_en, description_uz,
                images, map_url, latitude, longitude, schedule_json
            ) VALUES (
                $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13
            );
            """
            for r in TEST_DATA:
                await conn.execute(
                    insert_sql,
                    r["city"], r["interest"],
                    r["title_ru"], r["title_en"], r["title_uz"],
                    r["description_ru"], r["description_en"], r["description_uz"],
                    json.dumps(r["images"]),
                    r["map_url"], r["latitude"], r["longitude"],
                    json.dumps(r["schedule_json"]) if r["schedule_json"] is not None else None,
                )

async def get_routes_by_city_and_interest(city: str, interest: str, lang: str):
    if lang not in ("ru", "en", "uz"):
        lang = "ru"

    sql = """
    SELECT id, title_ru, title_en, title_uz,
           description_ru, description_en, description_uz,
           images, map_url, latitude, longitude, schedule_json
    FROM routes
    WHERE city = $1 AND interest = $2
    ORDER BY id;
    """
    async with POOL.acquire() as conn:
        rows = await conn.fetch(sql, city, interest)

    out = []
    for row in rows:
        out.append({
            "id": row["id"],
            "title": row[{"ru": "title_ru", "en": "title_en", "uz": "title_uz"}[lang]],
            "description": row[{"ru": "description_ru", "en": "description_en", "uz": "description_uz"}[lang]],
            "images": row["images"] or [],
            "map_url": row["map_url"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "schedule": row["schedule_json"],
        })
    return out

async def get_route_by_id(route_id: int, lang: str):
    if lang not in ("ru", "en", "uz"):
        lang = "ru"

    sql = """
    SELECT title_ru, title_en, title_uz,
           description_ru, description_en, description_uz,
           images, map_url, latitude, longitude, schedule_json
    FROM routes
    WHERE id = $1;
    """
    async with POOL.acquire() as conn:
        row = await conn.fetchrow(sql, route_id)
    if not row:
        return None

    return {
        "title": row[{"ru": "title_ru", "en": "title_en", "uz": "title_uz"}[lang]],
        "description": row[{"ru": "description_ru", "en": "description_en", "uz": "description_uz"}[lang]],
        "images": row["images"] or [],
        "map_url": row["map_url"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "schedule": row["schedule_json"],
    }
