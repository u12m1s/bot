import sqlite3

def seed_routes():
    conn = sqlite3.connect("routes.db")
    cursor = conn.cursor()

    routes = [
        (
            "Tashkent", "history",
            "Музей истории Узбекистана",
            "Museum of History of Uzbekistan",
            "O‘zbekiston tarixi muzeyi",
            41.3121, 69.2787
        ),
        (
            "Samarkand", "culture",
            "Регистан — сердце Самарканда",
            "Registan — heart of Samarkand",
            "Registon — Samarqand yuragi",
            39.6542, 66.9597
        ),
        (
            "Bukhara", "architecture",
            "Минарет Калян — символ Бухары",
            "Kalyan Minaret — symbol of Bukhara",
            "Kalon minorasi — Buxoro timsoli",
            39.7747, 64.4286
        )
    ]

    cursor.executemany("""
        INSERT INTO routes (
            city, interest,
            description_ru, description_en, description_uz,
            latitude, longitude
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, routes)

    conn.commit()
    conn.close()
    print("✅ Маршруты добавлены в базу.")

if __name__ == "__main__":
    seed_routes()
