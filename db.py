import aiosqlite
from pathlib import Path

# Путь до SQLite
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "routes.db"


async def init_db():
    """Инициализация базы"""
    async with aiosqlite.connect(DB_PATH) as conn:
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


async def get_routes_by_city_and_interest(city: str, interest: str):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "SELECT id, city, interest, description_ru, description_en, description_uz "
            "FROM routes WHERE city = ? AND interest = ?",
            (city, interest)
        )
        return await cursor.fetchall()


async def get_route_by_id(route_id: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "SELECT id, city, interest, description_ru, description_en, description_uz "
            "FROM routes WHERE id = ?",
            (route_id,)
        )
        return await cursor.fetchone()

