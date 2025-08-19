import asyncio
from db import init_db, add_route

# Список маршрутов для загрузки
ROUTES = [
    # city, interest, description_ru, description_en, description_uz
    ("Ташкент", "history", "Исторический маршрут по Ташкенту", "Historical route in Tashkent", "Toshkentdagi tarixiy yo'nalish"),
    ("Ташкент", "nature", "Природные достопримечательности Ташкента", "Nature sights in Tashkent", "Toshkentdagi tabiiy joylar"),
    ("Самарканд", "history", "Исторические места Самарканда", "Historical sites in Samarkand", "Samarqanddagi tarixiy joylar"),
    ("Бухара", "history", "Исторический маршрут по Бухаре", "Historical route in Bukhara", "Buxorodagi tarixiy yo'nalish")
]

async def main():
    await init_db()
    for city, interest, ru, en, uz in ROUTES:
        await add_route(city, interest, ru, en, uz)
        print(f"✅ Добавлен маршрут: {city} - {interest}")

    print("🎉 Все маршруты загружены!")

if __name__ == "__main__":
    asyncio.run(main())

