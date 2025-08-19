import asyncio
from db import init_db, add_route


async def seed():
    # Создаем таблицу, если ещё нет
    await init_db()

    # -------- Ташкент -------- #
    await add_route(
        "Ташкент", "история",
        "Посетите ансамбль Хазрати Имам, медресе Кукельдаш и старый город с его узкими улочками.",
        "Visit the Hazrati Imam complex, Kukeldash madrasah, and the Old Town with its narrow streets.",
        "Hazrati Imom majmuasi, Ko‘kaldosh madrasasi va tor ko‘chalari bilan Eski shaharni ziyorat qiling."
    )
    await add_route(
        "Ташкент", "культура",
        "Зайдите в Государственный музей истории Узбекистана и театр имени Навои.",
        "Visit the State Museum of History of Uzbekistan and the Navoi Theater.",
        "O‘zbekiston tarixi davlat muzeyi va Navoiy teatriga tashrif buyuring."
    )
    await add_route(
        "Ташкент", "природа",
        "Прогуляйтесь по Ташкентскому ботаническому саду и парку Анхор Локомотив.",
        "Take a walk through the Tashkent Botanical Garden and Anhor Lokomotiv Park.",
        "Toshkent botanika bog‘i va Anhor Lokomotiv bog‘ida sayr qiling."
    )

    # -------- Самарканд -------- #
    await add_route(
        "Самарканд", "история",
        "Площадь Регистан, мавзолей Гур-Эмир и некрополь Шахи-Зинда.",
        "Registan Square, Gur-Emir Mausoleum, and Shah-i-Zinda necropolis.",
        "Registon maydoni, Go‘ri Amir maqbarasi va Shohi Zinda majmuasi."
    )
    await add_route(
        "Самарканд", "культура",
        "Обсерватория Улугбека и музей Афросиаб.",
        "Ulugh Beg Observatory and Afrasiyab Museum.",
        "Ulug‘bek rasadxonasi va Afrosiyob muzeyi."
    )
    await add_route(
        "Самарканд", "природа",
        "Съездите на Чор-Чинор в Ургуте — древняя роща платанов.",
        "Visit Chor-Chinor in Urgut — an ancient plane tree grove.",
        "Urgutdagi Chor-Chinor — qadimiy chinorlar bog‘iga tashrif buyuring."
    )

    # -------- Бухара -------- #
    await add_route(
        "Бухара", "история",
        "Арк, минарет Калян и Ляби-Хауз.",
        "The Ark Fortress, Kalyan Minaret, and Lyabi-Hauz.",
        "Ark qal’asi, Kalon minorasi va Lyabi Hovuz majmuasi."
    )
    await add_route(
        "Бухара", "культура",
        "Медресе Мири-Араб и купольные базары.",
        "Mir-i-Arab Madrasah and the domed bazaars.",
        "Mir Arab madrasasi va gumbazli bozorlarga tashrif buyuring."
    )
    await add_route(
        "Бухара", "природа",
        "Прогуляйтесь по Ситораи Мохи-Хоса — летней резиденции эмира.",
        "Walk through Sitorai Mohi Hosa — the summer residence of the Emir.",
        "Amirning yozgi qarorgohi — Sitorai Mohi Xosa bog‘ida sayr qiling."
    )

    # -------- Хива -------- #
    await add_route(
        "Хива", "история",
        "Ичан-Кала, медресе Мухаммада Амин-хана и минарет Ислам-Ходжа.",
        "Ichan-Kala, Muhammad Amin-Khan Madrasah, and Islam-Khoja Minaret.",
        "Ichan Qal’a, Muhammad Aminxon madrasasi va Islom Xo‘ja minorasi."
    )
    await add_route(
        "Хива", "культура",
        "Караван-сараи и мастерские ремесленников внутри Ичан-Калы.",
        "Caravanserais and artisan workshops inside Ichan-Kala.",
        "Ichan Qal’a ichidagi karvonsaroylar va hunarmandchilik ustaxonalari."
    )
    await add_route(
        "Хива", "природа",
        "Прогуляйтесь по старым улочкам Ичан-Калы и насладитесь видом заката.",
        "Stroll through the old streets of Ichan-Kala and enjoy the sunset view.",
        "Ichan Qal’a qadimiy ko‘chalarida sayr qiling va quyosh botishini tomosha qiling."
    )

    print("🌍 База успешно заполнена маршрутами!")


if __name__ == "__main__":
    asyncio.run(seed())

