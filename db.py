import aiosqlite
import json # Potentially useful if you store JSON in DB, like for 'images'

DB_PATH = "routes.db"  # Path to your database file

async def get_routes_by_city_and_interest(city: str, interest: str, lang: str) -> list[dict]:
    """
    Retrieves routes from the database based on city, interest type, and language.
    'interest' here should be the generic type (e.g., 'nature', 'history', 'food').
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.cursor()

        # Ensure interest is the generic type stored in the DB (e.g., 'nature')
        # This mapping is important if user selects "🌳 Природа" but DB stores "nature"
        # We assume 'interest' parameter coming here is already the generic type (e.g., 'nature')
        # as handled in bot.py's process_interest function.

        description_column = f"description_{lang}"
        title_column = f"title_{lang}"

        query = f"""
            SELECT id, {title_column} AS title, {description_column} AS description, images, map_url, latitude, longitude
            FROM routes
            WHERE city_name_en=? AND interest_type=? AND {description_column} IS NOT NULL
        """
        await cursor.execute(query, (city.lower(), interest.lower())) # Ensure city and interest are lowercase for consistency
        rows = await cursor.fetchall()

        # Convert rows to list of dictionaries for easier access
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

async def get_route_by_id(route_id: int, lang: str) -> dict | None:
    """
    Retrieves a single route from the database by its ID and language.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.cursor()
        description_column = f"description_{lang}"
        title_column = f"title_{lang}"

        query = f"""
            SELECT id, {title_column} AS title, {description_column} AS description, images, map_url, latitude, longitude
            FROM routes
            WHERE id=?
        """
        await cursor.execute(query, (route_id,))
        row = await cursor.fetchone()

        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None


