import logging
import asyncio
from aiohttp import web
import os
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,
    FSInputFile, ReplyKeyboardRemove, CallbackQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart

from config import BOT_TOKEN
from db import init_db, get_routes_by_city_and_interest

# --- Логирование ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Инициализация бота ---
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# --- FSM ---
class StateGroup(StatesGroup):
    language = State()
    city = State()
    interest = State()
    route = State()

# --- Локализация ---
TRANSLATIONS = {
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "choose_language": {"ru": "Выберите язык:", "en": "Choose language:", "uz": "Tilni tanlang:"},
    "choose_city": {"ru": "📍 Выберите город:", "en": "📍 Choose a city:", "uz": "📍 Shaharni tanlang:"},
    "choose_interest": {"ru": "💡 Что вам интересно?", "en": "💡 What are you interested in?", "uz": "💡 Sizni nima qiziqtiradi?"},
    "cities": {"ru": ["Ташкент","Самарканд","Бухара"], "en": ["Tashkent","Samarkand","Bukhara"], "uz": ["Toshkent","Samarqand","Buxoro"]},
    "interests": {"ru":["🌳 Природа","🏛 История"], "en":["🌳 Nature","🏛 History"], "uz":["🌳 Tabiat","🏛 Tarix"]},
    "invalid_selection": {"ru": "Выберите вариант из кнопок", "en":"Please select from buttons","uz":"Tugmalardan birini tanlang"},
    "no_routes": {"ru":"Маршруты недоступны","en":"No routes available","uz":"Yo'nalishlar mavjud emas"},
    "choose_route": {"ru":"Выберите маршрут:","en":"Choose a route:","uz":"Yo'nalishni tanlang:"},
    "route_not_found": {"ru":"Маршрут не найден","en":"Route not found","uz":"Yo'nalish topilmadi"}
}

def t(key: str, lang: str) -> str:
    return TRANSLATIONS.get(key, {}).get(lang, key)

# --- Handlers ---
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    lang_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("🇷🇺 Русский"), KeyboardButton("🇬🇧 English")],
                  [KeyboardButton("🇺🇿 O'zbek")]],
        resize_keyboard=True
    )
    await message.answer(t("choose_language", "ru"), reply_markup=lang_keyboard)
    await state.set_state(StateGroup.language)

@dp.message(StateGroup.language)
async def choose_language(message: Message, state: FSMContext):
    lang_map = {"🇷🇺 Русский":"ru","🇬🇧 English":"en","🇺🇿 O'zbek":"uz"}
    lang = lang_map.get(message.text)
    if not lang:
        await message.answer(t("invalid_selection", "ru"))
        return
    await state.update_data(lang=lang)

    city_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=city)] for city in TRANSLATIONS["cities"][lang]] + [[KeyboardButton(t("back", lang))]],
        resize_keyboard=True
    )
    await message.answer(t("choose_city", lang), reply_markup=city_keyboard)
    await state.set_state(StateGroup.city)

@dp.message(StateGroup.city)
async def choose_city(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang","ru")
    if message.text == t("back", lang):
        await start(message, state)
        return
    city_list = TRANSLATIONS["cities"][lang]
    if message.text not in city_list:
        await message.answer(t("invalid_selection", lang))
        return
    await state.update_data(city=message.text)

    interest_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=i) for i in TRANSLATIONS["interests"][lang]]] + [[KeyboardButton(t("back", lang))]],
        resize_keyboard=True
    )
    await message.answer(t("choose_interest", lang), reply_markup=interest_keyboard)
    await state.set_state(StateGroup.interest)

@dp.message(StateGroup.interest)
async def choose_interest(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang","ru")
    if message.text == t("back", lang):
        await choose_city(message, state)
        return
    if message.text not in TRANSLATIONS["interests"][lang]:
        await message.answer(t("invalid_selection", lang))
        return

    await state.update_data(interest=message.text)
    city = data.get("city")
    interest = message.text

    # Получаем маршруты из db.py
    routes = await get_routes_by_city_and_interest(city, interest)
    if not routes:
        await message.answer(t("no_routes", lang))
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=f"Маршрут {r[0]}", callback_data=f"route_{r[0]}")] for r in routes]
    )
    await message.answer(t("choose_route", lang), reply_markup=keyboard)
    await state.set_state(StateGroup.route)

# --- Webapp для Render ---
async def health(request):
    return web.Response(text="ok")

async def start_webapp():
    app = web.Application()
    app.add_routes([web.get("/", health), web.get("/healthz", health)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "10000"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- Main ---
async def main():
    await init_db()
    await start_webapp()
    logging.info("✅ Bot is running")

if __name__ == "__main__":
    asyncio.run(main())
