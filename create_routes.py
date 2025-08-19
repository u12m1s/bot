import asyncpg
import asyncio
import os

# PostgreSQL connection settings
DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "database": os.getenv("POSTGRES_DB", "routes_db"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}


async def create_database():
    """Create PostgreSQL database and table"""
    # First connect without specifying a database to create the database
    admin_conn = await asyncpg.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"]
    )

    try:
        # Create database if it doesn't exist
        await admin_conn.execute(
            f"CREATE DATABASE {DB_CONFIG['database']} OWNER {DB_CONFIG['user']}"
        )
    except asyncpg.DuplicateDatabaseError:
        print("Database already exists")
    finally:
        await admin_conn.close()

    # Now connect to the new database to create tables
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        await conn.execute("""
                           CREATE TABLE IF NOT EXISTS routes
                           (
                               id             SERIAL PRIMARY KEY,
                               city           TEXT NOT NULL,
                               interest       TEXT NOT NULL,
                               description_ru TEXT,
                               description_en TEXT,
                               description_uz TEXT,
                               latitude       REAL,
                               longitude      REAL
                           )
                           """)
        print("✅ Database and table successfully created.")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(create_database())
