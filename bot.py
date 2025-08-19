import logging
import asyncio
from aiohttp import web
import json
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    CallbackQuery,
    ReplyKeyboardRemove,
    Location
)
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from config import BOT_TOKEN
from db import get_routes_by_city_and_interest, get_route_by_id, init_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Инициализация бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Состояния FSM
class StateGroup(StatesGroup):
    language = State()
    city = State()
    interest = State()
    place = State()  # Новое состояние
    route = State()
    viewing_route_details = State()

# Локализация
TRANSLATIONS = {
    # Основные команды
    "back": {
        "ru": "🔙 Назад",
        "en": "🔙 Back",
        "uz": "🔙 Orqaga"
    },
    "choose_language": {
        "ru": "Выберите язык:",
        "en": "Choose language:",
        "uz": "Tilni tanlang:"
    },
    "choose_city": {
        "ru": "📍 Выберите город:",
        "en": "📍 Choose a city:",
        "uz": "📍 Shaharni tanlang:"
    },
    "choose_interest": {
        "ru": "💡 Что вам интересно?",
        "en": "💡 What are you interested in?",
        "uz": "💡 Sizni nima qiziqtiradi?"
    },

    # Категории интересов
    "interests": {
        "ru": {
            "🌳 Природа": ["Чарвакское водохранилище", "Горы Чимган", "Ботанический сад"],
            "🏛 История": ["Регистан", "Гур-Эмир", "Шахи-Зинда"],
            "🍽 Еда": ["Ресторан Caravan", "Чайхана Нодирбек", "Лабзар"],
            "🛍 Шопинг": ["Чорсу базар", "Самарканд Дарвоза", "Малика"],
            "🎭 Культура": ["Театр Навои", "Кукольный театр", "Государственная консерватория"],
            "🏨 Отели": ["Хилтон Ташкент", "Самарканд Плаза", "Бухара Палас"]
        },
        "en": {
            "🌳 Nature": ["Charvak Reservoir", "Chimgan Mountains", "Botanical Garden"],
            "🏛 History": ["Registan", "Gur-Emir", "Shahi-Zinda"],
            "🍽 Food": ["Caravan Restaurant", "Nodirbek Tea House", "Labzar"],
            "🛍 Shopping": ["Chorsu Bazaar", "Samarkand Darvoza", "Malika"],
            "🎭 Culture": ["Navoi Theater", "Puppet Theater", "State Conservatory"],
            "🏨 Hotels": ["Hilton Tashkent", "Samarkand Plaza", "Bukhara Palace"]
        },
        "uz": {
            "🌳 Tabiat": ["Charvoq suv ombori", "Chimgan tog'lari", "Botanika bog'i"],
            "🏛 Tarix": ["Registon", "Gur-i Amir", "Shohi Zinda"],
            "🍽 Taom": ["Caravan restorani", "Nodirbek choyxonasi", "Labzar"],
            "🛍 Xarid": ["Chorsu bozori", "Samarqand Darvoza", "Malika"],
            "🎭 Madaniyat": ["Navoiy teatri", "Qo'g'irchoq teatri", "Davlat konservatoriyasi"],
            "🏨 Mehmonxonalar": ["Hilton Toshkent", "Samarqand Plaza", "Buxoro Palace"]
        }
    },

    # Соответствие категорий типам в БД
    "interest_to_db_type": {
        "🌳 Природа": "nature", "🌳 Nature": "nature", "🌳 Tabiat": "nature",
        "🏛 История": "history", "🏛 History": "history", "🏛 Tarix": "history",
        "🍽 Еда": "food", "🍽 Food": "food", "🍽 Taom": "food",
        "🛍 Шопинг": "shopping", "🛍 Shopping": "shopping", "🛍 Xarid": "shopping",
        "🎭 Культура": "culture", "🎭 Culture": "culture", "🎭 Madaniyat": "culture",
        "🏨 Отели": "hotels", "🏨 Hotels": "hotels", "🏨 Mehmonxonalar": "hotels"
    },

    # Города
    "cities": {
        "ru": ["Ташкент", "Самарканд", "Бухара", "Хива", "Фергана", "Нукус"],
        "en": ["Tashkent", "Samarkand", "Bukhara", "Khiva", "Fergana", "Nukus"],
        "uz": ["Toshkent", "Samarqand", "Buxoro", "Xiva", "Farg'ona", "Nukus"]
    },

    # Сообщения
    "no_routes": {
        "ru": "😕 Маршруты пока недоступны. Попробуйте другой выбор.",
        "en": "😕 No routes available. Try another option.",
        "uz": "😕 Yo'nalishlar mavjud emas. Boshqa variantni sinab ko'ring."
    },
    "choose_route": {
        "ru": "📌 Выберите маршрут:",
        "en": "📌 Choose a route:",
        "uz": "📌 Yo'nalishni tanlang:"
    },
    "route_not_found": {
        "ru": "❌ Маршрут не найден.",
        "en": "❌ Route not found.",
        "uz": "❌ Yo'nalish topilmadi."
    },
    "invalid_selection": {
        "ru": "Пожалуйста, выберите вариант из предложенных кнопок.",
        "en": "Please select an option from the provided buttons.",
        "uz": "Iltimos, taklif qilingan tugmalardan birini tanlang."
    },

    # Навигация
    "back_to_routes": {
        "ru": "🔙 К выбору маршрута",
        "en": "🔙 Back to Routes",
        "uz": "🔙 Yo'nalishlarni tanlashga"
    },
    "back_to_interest_selection": {
        "ru": "🔙 К интересам",
        "en": "🔙 Back to Interests",
        "uz": "🔙 Qiziqishlarga qaytish"
    },

    # Дополнительные элементы
    "photo_not_available": {
        "ru": "📷 Фото недоступно",
        "en": "📷 Photo not available",
        "uz": "📷 Rasm mavjud emas"
    },
    "schedule": {
        "ru": "⏳ Расписание",
        "en": "⏳ Schedule",
        "uz": "⏳ Jadval"
    },
    "working_hours": {
        "ru": "🕒 Часы работы",
        "en": "🕒 Working hours",
        "uz": "🕒 Ish vaqti"
    },
    "difficulty": {
        "ru": "⚡ Сложность",
        "en": "⚡ Difficulty",
        "uz": "⚡ Qiyinchilik"
    },
    "price_range": {
        "ru": "💲 Ценовой диапазон",
        "en": "💲 Price range",
        "uz": "💲 Narxlar"
    },

    # Новые функции
    "detailed_history": {
        "ru": "📜 Подробная история",
        "en": "📜 Detailed history",
        "uz": "📜 Batafsil tarix"
    },
    "show_on_map": {
        "ru": "🗺️ Показать на карте",
        "en": "🗺️ Show on map",
        "uz": "🗺️ Xaritada ko'rsatish"
    },
    "contact_info": {
        "ru": "📞 Контакты",
        "en": "📞 Contacts",
        "uz": "📞 Kontaktlar"
    },
    "reviews": {
        "ru": "⭐ Отзывы",
        "en": "⭐ Reviews",
        "uz": "⭐ Sharhlar"
    },

    # Валидация
    "invalid_language": {
        "ru": "Пожалуйста, выберите язык из предложенных:",
        "en": "Please select a language from the options:",
        "uz": "Iltimos, quyidagi tillardan birini tanlang:"
    },

    # Категории сложности
    "difficulty_levels": {
        "ru": ["Легкая", "Средняя", "Сложная"],
        "en": ["Easy", "Medium", "Hard"],
        "uz": ["Oson", "O'rtacha", "Qiyin"]
    },

    # Ценовые диапазоны
    "price_levels": {
        "ru": ["💰 Бюджетный", "💰💰 Средний", "💰💰💰 Премиум"],
        "en": ["💰 Budget", "💰💰 Mid-range", "💰💰💰 Premium"],
        "uz": ["💰 Arzon", "💰💰 O'rtacha", "💰💰💰 Premium"]
    }
}
def t(key: str, lang: str) -> str:
    """Получение перевода по ключу и языку"""
    return TRANSLATIONS.get(key, {}).get(lang, key)

# --- Handlers ---
@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Обработка команды /start"""
    await state.clear()
    lang_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")],
            [KeyboardButton(text="🇺🇿 O'zbek")]
        ],
        resize_keyboard=True
    )
    await message.answer(t("choose_language", "ru"), reply_markup=lang_keyboard)
    await state.set_state(StateGroup.language)


@dp.message(StateGroup.language)
async def choose_language(message: Message, state: FSMContext):
    """Обработка выбора языка без дублирования"""
    lang_map = {
        "🇷🇺 Русский": "ru",
        "🇬🇧 English": "en",
        "🇺🇿 O'zbek": "uz"
    }

    lang = lang_map.get(message.text)
    if not lang:
        await message.answer("Пожалуйста, выберите язык из предложенных кнопок")
        return

    await state.update_data(lang=lang)

    # Получаем список городов для выбранного языка
    cities = TRANSLATIONS["cities"][lang]

    city_keyboard = ReplyKeyboardMarkup(
        keyboard=[
                     [KeyboardButton(text=city)] for city in cities
                 ] + [
                     [KeyboardButton(text=t("back", lang))]
                 ],
        resize_keyboard=True
    )

    await message.answer(
        t("choose_city", lang),
        reply_markup=city_keyboard
    )
    await state.set_state(StateGroup.city)


@dp.message(StateGroup.city)
async def process_city(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    if message.text == t("back", lang):
        await start_command(message, state)
        return

    # Проверяем город на всех языках
    city_mapping = {
        "ru": {"Ташкент": "tashkent", "Самарканд": "samarkand", "Бухара": "bukhara", "Хива": "khiva",
               "Фергана": "fergana", "Нукус": "nukus"},
        "en": {"Tashkent": "tashkent", "Samarkand": "samarkand", "Bukhara": "bukhara", "Khiva": "khiva",
               "Fergana": "fergana", "Nukus": "nukus"},
        "uz": {"Toshkent": "tashkent", "Samarqand": "samarkand", "Buxoro": "bukhara", "Xiva": "khiva",
               "Farg'ona": "fergana", "Nukus": "nukus"}
    }

    city_name = message.text.strip()
    city_key = None

    for lang_code in city_mapping:
        if city_name in city_mapping[lang_code]:
            city_key = city_mapping[lang_code][city_name]
            break

    if not city_key:
        await message.answer(t("invalid_selection", lang))
        return

    await state.update_data(city=city_key)

    # Создаем клавиатуру с интересами
    interest_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=interest) for interest in TRANSLATIONS["interests"][lang].keys()],
            [KeyboardButton(text=t("back", lang))]
        ],
        resize_keyboard=True
    )

    await message.answer(t("choose_interest", lang), reply_markup=interest_keyboard)
    await state.set_state(StateGroup.interest)


@dp.message(StateGroup.interest)
async def process_interest(message: Message, state: FSMContext):
    """Обработка выбора интереса"""
    data = await state.get_data()
    lang = data.get("lang", "ru")

    if message.text == t("back", lang):
        # Возвращаемся к выбору города
        cities = TRANSLATIONS["cities"][lang]
        city_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                         [KeyboardButton(text=city)] for city in cities
                     ] + [
                         [KeyboardButton(text=t("back", lang))]
                     ],
            resize_keyboard=True
        )
        await message.answer(t("choose_city", lang), reply_markup=city_keyboard)
        await state.set_state(StateGroup.city)
        return

    # Получаем соответствие между текстом кнопки и типом в БД
    interest_text = message.text
    db_interest = TRANSLATIONS["interest_to_db_type"].get(interest_text)

    if not db_interest:
        await message.answer(t("invalid_selection", lang))
        return

    await state.update_data(interest_type=db_interest)

    # Получаем данные для маршрутов
    city = data.get("city")
    routes = await get_routes_by_city_and_interest(city, db_interest, lang)

    if not routes:
        await message.answer(t("no_routes", lang))
        return

    # Создаем клавиатуру с маршрутами (убираем ReplyKeyboardMarkup)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                            [InlineKeyboardButton(text=route["title"], callback_data=f"route_{route['id']}")]
                            for route in routes
                        ] + [[
            InlineKeyboardButton(
                text=t("back_to_interest_selection", lang),
                callback_data="back_to_interests"
            )
        ]]
    )

    # Отправляем сообщение с инлайн-клавиатурой и убираем ReplyKeyboard
    await message.answer(
        t("choose_route", lang),
        reply_markup=ReplyKeyboardRemove()  # Это убирает меню кнопок внизу
    )
    await message.answer(
        t("choose_route", lang),
        reply_markup=keyboard
    )
    await state.set_state(StateGroup.route)
    await state.set_state(StateGroup.route)

@dp.callback_query(F.data.startswith("route_"))
async def show_route_details(callback: CallbackQuery, state: FSMContext):
    """Показ деталей маршрута"""
    await callback.answer()
    route_id = int(callback.data.split("_")[1])
    data = await state.get_data()
    lang = data.get("lang", "ru")

    route = await get_route_by_id(route_id, lang)
    if not route:
        await callback.message.answer(t("route_not_found", lang))
        return

    # Отправка фотографий
    for photo_path in route["images"]:
        try:
            if os.path.exists(photo_path):
                await callback.message.answer_photo(FSInputFile(photo_path))
            else:
                logging.warning(f"Photo not found: {photo_path}")
                await callback.message.answer("📷 " + t("photo_not_available", lang))
        except Exception as e:
            logging.error(f"Error sending photo: {e}")

    # Подготовка текста маршрута
    route_text = f"<b>{route['title']}</b>\n\n{route['description']}"

    if route.get("schedule"):
        schedule_text = f"\n\n⏳ <b>{t('schedule', lang)}:</b>\n"
        for item in route["schedule"]:
            schedule_text += f"• {item['time']} - {item[f'activity_{lang}']}\n"
        route_text += schedule_text

    await callback.message.answer(
        route_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text=t("back_to_routes", lang),
                callback_data="back_to_routes"
            )
        ]])
    )

    # Отправка локации для Чарвака/Чимгана
    if route.get('latitude') and route.get('longitude'):
        try:
            await callback.message.answer_location(
                latitude=route['latitude'],
                longitude=route['longitude']
            )
        except Exception as e:
            logging.error(f"Error sending location: {e}")

@dp.callback_query(F.data == "back_to_routes")
async def back_to_routes_list(callback: CallbackQuery, state: FSMContext):
    """Возврат к списку маршрутов"""
    await callback.answer()
    data = await state.get_data()
    lang = data.get("lang", "ru")
    city = data.get("city")
    interest_type = data.get("interest_type")

    if not city or not interest_type:
        await callback.message.answer("Please select your preferences again")
        await state.set_state(StateGroup.interest)
        return

    routes = await get_routes_by_city_and_interest(city, interest_type, lang)

    if not routes:
        await callback.message.answer(t("no_routes", lang))
        await back_to_interests(callback, state)
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=route["title"], callback_data=f"route_{route['id']}")]
            for route in routes
        ] + [[
            InlineKeyboardButton(
                text=t("back_to_interest_selection", lang),
                callback_data="back_to_interests"
            )
        ]]
    )

    await callback.message.answer(t("choose_route", lang), reply_markup=keyboard)
    await state.set_state(StateGroup.route)

@dp.callback_query(F.data == "back_to_interests")
async def back_to_interests(callback: CallbackQuery, state: FSMContext):
    """Возврат к выбору интересов"""
    await callback.answer()
    data = await state.get_data()
    lang = data.get("lang", "ru")

    # Удаляем предыдущее сообщение с инлайн-клавиатурой
    await callback.message.delete()

    interest_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=interest) for interest in TRANSLATIONS["interests"][lang]],
            [KeyboardButton(text=t("back", lang))]
        ],
        resize_keyboard=True
    )
    await callback.message.answer(
        t("choose_interest", lang),
        reply_markup=interest_keyboard
    )
    await state.set_state(StateGroup.interest)


@dp.message(StateGroup.place)
async def process_place(message: Message, state: FSMContext):
    """Обработка выбора конкретного места"""
    data = await state.get_data()
    lang = data.get("lang", "ru")

    if message.text == t("back", lang):
        await state.set_state(StateGroup.interest)
        interest_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                         [KeyboardButton(text=category)] for category in TRANSLATIONS["interests"][lang]
                     ] + [
                         [KeyboardButton(text=t("back", lang))]
                     ],
            resize_keyboard=True
        )
        await message.answer(t("choose_interest", lang), reply_markup=interest_keyboard)
        return

    # Здесь можно добавить логику для обработки конкретного места
    await message.answer(f"Вы выбрали: {message.text}")
    # Дальнейшая обработка...


async def health(request):
    return web.Response(text="ok")

async def start_webapp():
    app = web.Application()
    app.add_routes([web.get("/", health), web.get("/healthz", health)])
    runner = web.AppRunner(app)
    await runner.setup()
    import os
    port = int(os.getenv("PORT", "10000"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

from db import init_db, add_route, get_routes_by_city_and_interest

async def main():
    await init_db()
    await add_route("Ташкент", "history", "Описание RU", "Description EN", "Tavsif UZ")
    routes = await get_routes_by_city_and_interest("Ташкент", "history")
    print(routes)



if __name__ == "__main__":
    asyncio.run(main())