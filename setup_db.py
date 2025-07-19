import sqlite3
import os
import json

# Define the path to your database file
DB_PATH = "routes.db"

# Define the path to your photos directory
PHOTOS_DIR = "photos"

# Ensure the photos directory exists
if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)
    print(f"Created directory: {PHOTOS_DIR}")

def setup_database():
    """
    Connects to the SQLite database, creates the 'routes' table if it doesn't exist,
    and inserts example data.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # SQL to create the 'routes' table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name_en TEXT NOT NULL,         -- e.g., 'tashkent', 'samarkand' (English, for consistent lookup)
            interest_type TEXT NOT NULL,        -- 'nature', 'history', 'food' (generic type)
            title_ru TEXT,                      -- Title in Russian
            title_en TEXT,                      -- Title in English
            title_uz TEXT,                      -- Title in Uzbek
            description_ru TEXT,                -- Description in Russian
            description_en TEXT,                -- Description in English
            description_uz TEXT,                -- Description in Uzbek
            images TEXT,                        -- JSON string of image paths, e.g., '["photos/charvak1.jpg", "photos/charvak2.jpg"]'
            map_url TEXT,                       -- Google Maps URL
            latitude REAL,
            longitude REAL
        );
        """
        cursor.execute(create_table_sql)
        print("Table 'routes' checked/created successfully.")

        # Example data to insert
        # IMPORTANT: Ensure these image paths correspond to actual files in your 'photos' directory.
        # If you don't have these specific images, replace them with placeholder paths or create them.
        example_routes = [
            # Tashkent - Nature
            ('tashkent', 'nature', 'Ботанический сад', 'Botanical Garden', 'Botanika bog‘i', 'Большой и красивый ботанический сад в Ташкенте. Идеальное место для прогулок и отдыха.', 'A large and beautiful botanical garden in Tashkent. Ideal place for walks and relaxation.', 'Toshkentdagi katta va chiroyli botanika bog‘i. Sayr qilish va dam olish uchun ajoyib joy.', json.dumps(["photos/tashkent/botanical_garden_1.jpg", "photos/tashkent/botanical_garden_2.jpg"]), 'https://maps.app.goo.gl/abcdefg1', 41.3524, 69.3091),
            ('tashkent', 'nature', 'Парк "Ашхабад"', 'Ashgabat Park', 'Ashxobod bog‘i', 'Современный парк с аттракционами и местами для отдыха, отличное место для семейного досуга.', 'A modern park with attractions and recreation areas, an excellent place for family leisure.', 'Attraksionlar va dam olish zonalari bo‘lgan zamonaviy bog‘, oilaviy dam olish uchun ajoyib joy.', json.dumps(["photos/tashkent/ashgabat_park_1.jpg"]), 'https://maps.app.goo.gl/abcdefg2', 41.2899, 69.3005),
            ('tashkent', 'nature', 'Японский сад', 'Japanese Garden', 'Yapon bog‘i', 'Тихий и умиротворяющий уголок природы в центре Ташкента, идеальный для релаксации.', 'A quiet and peaceful corner of nature in the center of Tashkent, ideal for relaxation.', 'Toshkent markazida tinch va osoyishta tabiat go‘shasi, dam olish uchun ideal joy.', json.dumps(["photos/tashkent/japanese_garden_1.jpg"]), 'https://maps.app.goo.gl/abcdefg3', 41.3190, 69.2900),

            # Tashkent - History
            ('tashkent', 'history', 'Музей Амира Темура', 'Amir Temur Museum', 'Amir Temur muzeyi', 'Музей, посвященный жизни и наследию великого полководца Амира Темура.', 'A museum dedicated to the life and legacy of the great commander Amir Temur.', 'Buyuk sarkarda Amir Temurning hayoti va merosiga bag‘ishlangan muzey.', json.dumps(["photos/tashkent/amir_temur_museum_1.jpg", "photos/tashkent/amir_temur_museum_2.jpg"]), 'https://maps.app.goo.gl/abcdefg4', 41.3159, 69.2817),
            ('tashkent', 'history', 'Комплекс Хаст-Имам', 'Hazrati Imam Complex', 'Hazrati Imom majmuasi', 'Исторический и духовный центр Ташкента, где хранится древний Коран Османа.', 'A historical and spiritual center of Tashkent, home to the ancient Uthman Quran.', 'Toshkentning tarixiy va ma‘naviy markazi, qadimiy Usmon Qur’oni saqlanadigan joy.', json.dumps(["photos/tashkent/hazrati_imam_1.jpg", "photos/tashkent/hazrati_imam_2.jpg"]), 'https://maps.app.goo.gl/abcdefg5', 41.3323, 69.2612),
            ('tashkent', 'history', 'Базар Чорсу', 'Chorsu Bazaar', 'Chorsu bozori', 'Один из старейших и крупнейших базаров в Центральной Азии, погружение в восточную атмосферу.', 'One of the oldest and largest bazaars in Central Asia, an immersion into the oriental atmosphere.', 'Markaziy Osiyodagi eng qadimgi va yirik bozorlardan biri, sharqona muhitga sho‘ng‘ish.', json.dumps(["photos/tashkent/chorsu_bazaar_1.jpg"]), 'https://maps.app.goo.gl/abcdefg6', 41.3350, 69.2390),

            # Tashkent - Food
            ('tashkent', 'food', 'Центр плова "Беш Казан"', 'Plov Center "Besh Kazan"', 'Osh Markazi "Besh Qozon"', 'Популярное место для дегустации настоящего узбекского плова в огромных казанах.', 'A popular place to taste authentic Uzbek plov cooked in huge cauldrons.', 'Haqiqiy o‘zbek palovini ulkan qozonlarda tatib ko‘rish uchun mashhur joy.', json.dumps(["photos/tashkent/plov_center_1.jpg"]), 'https://maps.app.goo.gl/abcdefg7', 41.3106, 69.2902),
            ('tashkent', 'food', 'Ресторан "Milliy Taomlar"', 'Restaurant "Milliy Taomlar"', 'Restoran "Milliy Taomlar"', 'Широкий выбор блюд национальной узбекской кухни в уютной атмосфере.', 'A wide selection of national Uzbek dishes in a cozy atmosphere.', 'Qulay muhitda milliy o‘zbek taomlarining keng tanlovi.', json.dumps(["photos/tashkent/milliy_taomlar_1.jpg"]), 'https://maps.app.goo.gl/abcdefg8', 41.2980, 69.2670),

            # Samarkand - History
            ('samarkand', 'history', 'Площадь Регистан', 'Registan Square', 'Registon Maydoni', 'Знаменитый архитектурный ансамбль, сердце Самарканда. Включает медресе Улугбека, Шердор и Тилля-Кари.', 'Famous architectural ensemble, the heart of Samarkand. Includes Ulugbek, Sher-Dor, and Tilya-Kori madrasahs.', 'Samarqandning yuragi, mashhur me‘moriy majmua. Ulug‘bek, Sherdor va Tillakori madrasalari kabi inshootlarni o‘z ichiga oladi.', json.dumps(["photos/samarkand/registan_1.jpg", "photos/samarkand/registan_2.jpg"]), 'https://maps.app.goo.gl/abcdefg9', 39.6540, 66.9740),
            ('samarkand', 'history', 'Мавзолей Гур-Эмир', 'Gur-Emir Mausoleum', 'Go‘ri Amir maqbarasi', 'Усыпальница Амира Темура и его потомков, шедевр средневековой архитектуры.', 'The mausoleum of Amir Temur and his descendants, a masterpiece of medieval architecture.', 'Amir Temur va uning avlodlarining maqbarasi, o‘rta asr me‘morchiligining durdonasi.', json.dumps(["photos/samarkand/gur_emir_1.jpg"]), 'https://maps.app.goo.gl/abcdefg10', 39.6450, 66.9730),
            ('samarkand', 'history', 'Мечеть Биби-Ханым', 'Bibi-Khanym Mosque', 'Bibixonim masjidi', 'Грандиозная соборная мечеть, построенная по приказу Амира Темура.', 'A grandiose congregational mosque built by the order of Amir Temur.', 'Amir Temur buyrug‘i bilan qurilgan ulkan jome masjidi.', json.dumps(["photos/samarkand/bibi_khanym_1.jpg"]), 'https://maps.app.goo.gl/abcdefg11', 39.6590, 66.9800),
            ('samarkand', 'history', 'Шахи Зинда', 'Shahi Zinda Necropolis', 'Shohi Zinda majmuasi', 'Ансамбль мавзолеев, где захоронены члены царской семьи и знати.', 'An ensemble of mausoleums where members of the royal family and nobility are buried.', 'Qirol oilasi va zodagonlar dafn etilgan maqbaralar majmuasi.', json.dumps(["photos/samarkand/shahi_zinda_1.jpg"]), 'https://maps.app.goo.gl/abcdefg12', 39.6640, 66.9770),

            # Samarkand - Food
            ('samarkand', 'food', 'Самаркандский плов', 'Samarkand Plov', 'Samarqand palovi', 'Попробуйте уникальный самаркандский плов, готовящийся по особому рецепту.', 'Taste the unique Samarkand plov, prepared according to a special recipe.', 'Maxsus retsept bo‘yicha tayyorlanadigan noyob Samarqand palovini tatib ko‘ring.', json.dumps(["photos/samarkand/samarkand_plov_1.jpg"]), 'https://maps.app.goo.gl/abcdefg13', 39.6600, 66.9750),

            # Bukhara - History
            ('bukhara', 'history', 'Комплекс Пои-Калян', 'Poi Kalyan Complex', 'Poi Kalyan majmuasi', 'Исторический комплекс в Бухаре, включающий минарет Калян, мечеть Калян и медресе Мири Араб.', 'Historical complex in Bukhara including Kalyan Minaret, Kalyan Mosque, and Mir-i-Arab Madrasah.', 'Buxorodagi tarixiy majmua, Qalyan minorasi, Qalyan masjidi va Mir-i-Arab madrasasi kabi inshootlarni o‘z ichiga oladi.', json.dumps(["photos/bukhara/poi_kalyan_1.jpg", "photos/bukhara/poi_kalyan_2.jpg"]), 'https://maps.app.goo.gl/abcdefg14', 39.7749, 64.4172),
            ('bukhara', 'history', 'Ляби-Хауз', 'Lyab-i Hauz Complex', 'Lyabi Hovuz majmuasi', 'Сердце старой Бухары, живописный ансамбль вокруг пруда с медресе и мечетями.', 'The heart of old Bukhara, a picturesque ensemble around a pond with madrasahs and mosques.', 'Eski Buxoroning yuragi, hovuz atrofidagi madrasa va masjidlar bilan go‘zal majmua.', json.dumps(["photos/bukhara/lyab_i_hauz_1.jpg"]), 'https://maps.app.goo.gl/abcdefg15', 39.7740, 64.4160),
            ('bukhara', 'history', 'Мавзолей Саманидов', 'Samanid Mausoleum', 'Somoniylar maqbarasi', 'Один из лучших образцов исламской архитектуры X века.', 'One of the finest examples of 10th-century Islamic architecture.', 'X asr Islom me‘morchiligining eng yaxshi namunalaridan biri.', json.dumps(["photos/bukhara/samanid_mausoleum_1.jpg"]), 'https://maps.app.goo.gl/abcdefg16', 39.7780, 64.4090),

            # Bukhara - Food
            ('bukhara', 'food', 'Бухарский плов', 'Bukhara Plov', 'Buxoro palovi', 'Отведайте уникальный бухарский плов, который отличается от других видов плова.', 'Taste the unique Bukhara plov, which differs from other types of plov.', 'Boshqa palov turlaridan farq qiladigan noyob Buxoro palovini tatib ko‘ring.', json.dumps(["photos/bukhara/bukhara_plov_1.jpg"]), 'https://maps.app.goo.gl/abcdefg17', 39.7755, 64.4165)
        ]

        # Check if the table is empty before inserting data
        cursor.execute("SELECT COUNT(*) FROM routes")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO routes (city_name_en, interest_type, title_ru, title_en, title_uz, description_ru, description_en, description_uz, images, map_url, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, example_routes)
            conn.commit()
            print("Example data inserted successfully.")
        else:
            print("Table 'routes' already contains data. Skipping insertion of example data.")
            # Optional: If you want to force re-insertion or update, you could TRUNCATE TABLE or DELETE FROM TABLE here,
            # but be careful as it will wipe all existing data.
            # Example to wipe and re-insert:
            # cursor.execute("DELETE FROM routes")
            # conn.commit()
            # cursor.executemany(...)
            # conn.commit()
            # print("Existing data cleared and new example data inserted successfully.")


    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    setup_database()