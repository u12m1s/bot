import os
import aiosqlite
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")  # Railway → PostgreSQL
pg_pool = None  # пул для PostgreSQL


async def init_db():
    global pg_pool

    if DATABASE_URL:
        # 🔹 PostgreSQL
        if pg_pool is None:
            pg_pool = await asyncpg.create_pool(DATABASE_URL)

        async with pg_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS routes (
                    id SERIAL PRIMARY KEY,
                    city TEXT,
                    interest TEXT,
                    description_ru TEXT,
                    description_en TEXT,
                    description_uz TEXT
                )
            """)
        print("✅ PostgreSQL initialized")
    else:
        # 🔹 SQLite (локальная разработка)
        async with aiosqlite.connect("routes.db") as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS routes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    interest TEXT,
                    description_ru TEXT,
                    description_en TEXT,
                    description_uz TEXT
                )
            """)
            await conn.commit()
        print("✅ SQLite initialized")


# -------- Запросы -------- #

async def add_route(city, interest, ru, en, uz):
    if DATABASE_URL:
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO routes (city, interest, description_ru, description_en, description_uz)
                   VALUES ($1, $2, $3, $4, $5)""",
                city, interest, ru, en, uz
            )
    else:
        async with aiosqlite.connect("routes.db") as conn:
            await conn.execute(
                """INSERT INTO routes (city, interest, description_ru, description_en, description_uz)
                   VALUES (?, ?, ?, ?, ?)""",
                (city, interest, ru, en, uz)
            )
            await conn.commit()


async def get_routes_by_city_and_interest(city, interest):
    if DATABASE_URL:
        async with pg_pool.acquire() as conn:
            rows = await conn.fetch(
                """SELECT id, city, interest, description_ru, description_en, description_uz
                   FROM routes WHERE city=$1 AND interest=$2""",
                city, interest
            )
        return rows
    else:
        async with aiosqlite.connect("routes.db") as conn:
            cursor = await conn.execute(
                """SELECT id, city, interest, description_ru, description_en, description_uz
                   FROM routes WHERE city=? AND interest=?""",
                (city, interest)
            )
            rows = await cursor.fetchall()
        return rows

