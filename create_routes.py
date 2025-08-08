import sqlite3

def create_database():
    conn = sqlite3.connect("routes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        interest TEXT NOT NULL,
        description_ru TEXT,
        description_en TEXT,
        description_uz TEXT,
        latitude REAL,
        longitude REAL
    );
    """)

    conn.commit()
    conn.close()
    print("✅ База данных успешно создана.")

if __name__ == "__main__":
    create_database()
