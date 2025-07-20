import logging
import asyncio
import json
import os
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    CallbackQuery,
    ReplyKeyboardRemove  # <-- Ensure this is imported
)
from aiogram.client.default import DefaultBotProperties

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart

from config import BOT_TOKEN
from db import get_routes_by_city_and_interest, get_route_by_id

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Bot setup
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())


# FSM States
class StateGroup(StatesGroup):
    language = State()
    city = State()
    interest = State()
    route = State()  # User is viewing a list of routes to choose from (inline keyboard shown, ReplyKeyboardRemove active)
    viewing_route_details = State()  # User is viewing details of a single route (inline keyboard shown, ReplyKeyboardRemove active)


# Translations dictionary
TRANSLATIONS = {
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "choose_language": {
        "ru": "Выберите язык / Choose language / Tilni tanlang:",
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
    "interests": {
        "ru": ["🌳 Природа", "🏛 История", "🍽 Еда"],
        "en": ["🌳 Nature", "🏛 History", "🍽 Food"],
        "uz": ["🌳 Tabiat", "🏛 Tarix", "🍽 Taom"]
    },
    "interest_to_db_type": {
        "🌳 Природа": "nature", "🌳 Nature": "nature", "🌳 Tabiat": "nature",
        "🏛 История": "history", "🏛 History": "history", "🏛 Tarix": "history",
        "🍽 Еда": "food", "🍽 Food": "food", "🍽 Taom": "food"
    },
    "cities": ["Tashkent", "Samarkand", "Bukhara"],
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
    "photo_error": {
        "ru": "Не удалось отправить одно или несколько фото.",
        "en": "Failed to send one or more photos.",
        "uz": "Bir yoki bir nechta fotosurat yuborib bo'lmadi."
    },
    "back_to_routes": {  # New translation for the inline "Back" button from route details
        "ru": "🔙 К выбору маршрута",
        "en": "🔙 Back to Routes",
        "uz": "🔙 Yo'nalishlarni tanlashga"
    },
    "back_to_interest_selection": {  # New translation for the inline "Back" from route list
        "ru": "🔙 К интересам",
        "en": "🔙 Back to Interests",
        "uz": "🔙 Qiziqishlarga qaytish"
    }
}


def t(key: str, lang: str) -> str:
    """Helper function for multi-language translations."""
    return TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get("ru", key))


# --- Handlers ---

@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Handles the /start command."""
    await state.clear()
    lang_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")],
            [KeyboardButton(text="🇺🇿 O'zbek")]
        ], resize_keyboard=True
    )
    await message.answer(t("choose_language", "ru"), reply_markup=lang_keyboard)
    await state.set_state(StateGroup.language)


@dp.message(StateGroup.language)
async def choose_language(message: Message, state: FSMContext):
    """Handles language selection."""
    lang_map = {
        "🇷🇺 Русский": "ru",
        "🇬🇧 English": "en",
        "🇺🇿 O'zbek": "uz"
    }
    lang = lang_map.get(message.text)

    if not lang:
        current_data = await state.get_data()
        current_lang = current_data.get("lang", "ru")
        await message.answer(t("invalid_selection", current_lang), reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")],
                [KeyboardButton(text="🇺🇿 O'zbek")]
            ], resize_keyboard=True
        ))
        return

    await state.update_data(lang=lang)
    city_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=city)] for city in TRANSLATIONS["cities"]] +
                 [[KeyboardButton(text=t("back", lang))]],  # Back button here
        resize_keyboard=True
    )
    await message.answer(t("choose_city", lang), reply_markup=city_keyboard)
    await state.set_state(StateGroup.city)


@dp.message(StateGroup.city)
async def process_city(message: Message, state: FSMContext):
    """Handles city selection."""
    data = await state.get_data()
    lang = data.get("lang", "ru")

    if message.text == t("back", lang):  # If Reply Keyboard "Back" is pressed
        await start_command(message, state)
        return

    city_name = message.text.strip()
    if city_name not in TRANSLATIONS["cities"]:
        await message.answer(t("invalid_selection", lang), reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=city)] for city in TRANSLATIONS["cities"]] +
                     [[KeyboardButton(text=t("back", lang))]],
            resize_keyboard=True
        ))
        return

    await state.update_data(city=city_name.lower())
    interest_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=TRANSLATIONS["interests"][lang][0]),
             KeyboardButton(text=TRANSLATIONS["interests"][lang][1])],
            [KeyboardButton(text=TRANSLATIONS["interests"][lang][2])],
            [KeyboardButton(text=t("back", lang))]  # Back button here
        ],
        resize_keyboard=True
    )
    await message.answer(t("choose_interest", lang), reply_markup=interest_keyboard)
    await state.set_state(StateGroup.interest)


@dp.message(StateGroup.interest)
async def process_interest(message: Message, state: FSMContext):
    """Handles interest selection (Nature, History, Food)."""
    data = await state.get_data()
    lang = data.get("lang", "ru")

    if message.text == t("back", lang):  # If Reply Keyboard "Back" is pressed
        city_keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=city)] for city in TRANSLATIONS["cities"]] +
                     [[KeyboardButton(text=t("back", lang))]],
            resize_keyboard=True
        )
        await message.answer(t("choose_city", lang), reply_markup=city_keyboard)
        await state.set_state(StateGroup.city)
        return

    selected_interest_label = message.text.strip()
    db_interest_type = TRANSLATIONS["interest_to_db_type"].get(selected_interest_label)

    if not db_interest_type:
        await message.answer(t("invalid_selection", lang), reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=TRANSLATIONS["interests"][lang][0]),
                 KeyboardButton(text=TRANSLATIONS["interests"][lang][1])],
                [KeyboardButton(text=TRANSLATIONS["interests"][lang][2])],
                [KeyboardButton(text=t("back", lang))]
            ], resize_keyboard=True
        ))
        return

    city = data.get("city")

    routes = await get_routes_by_city_and_interest(city, db_interest_type, lang)

    await state.update_data(interest=db_interest_type)

    if not routes:
        await message.answer(t("no_routes", lang))
        return

    inline_buttons = []
    for r in routes:
        inline_buttons.append([InlineKeyboardButton(text=r["title"], callback_data=f"route_{r['id']}")])

    # Add an inline back button to go back to interest selection from route list
    inline_buttons.append([InlineKeyboardButton(text=t("back_to_interest_selection", lang),
                                                callback_data="back_from_routes_to_interest")])

    # IMPORTANT: First, remove the ReplyKeyboardMarkup
    await message.answer(t("choose_route", lang), reply_markup=ReplyKeyboardRemove())
    # Then, send the message with the InlineKeyboardMarkup
    await message.answer(t("choose_route", lang), reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_buttons))
    await state.set_state(StateGroup.route)


@dp.callback_query(F.data.startswith("route_"))
async def show_route(callback: CallbackQuery, state: FSMContext):
    """Handles displaying a specific route's details."""
    await callback.answer()

    route_id = int(callback.data.split("_")[1])
    data = await state.get_data()
    lang = data.get("lang", "ru")

    route = await get_route_by_id(route_id, lang)

    if not route:
        await callback.message.answer(t("route_not_found", lang))
        return

    photos_json = route.get("images", "[]")
    photos = json.loads(photos_json)

    logging.info(f"Attempting to send photos for route ID: {route_id}")
    logging.info(f"Photos from DB JSON: {photos_json}")
    logging.info(f"Parsed photos list: {photos}")

    sent_photos_count = 0
    for photo_path in photos:
        full_path = os.path.join("photos", os.path.basename(photo_path))
        logging.info(f"Checking photo path: {full_path}")
        if os.path.exists(full_path):
            logging.info(f"File found: {full_path}")
            try:
                await callback.message.answer_photo(FSInputFile(full_path))
                sent_photos_count += 1
            except Exception as e:
                logging.error(f"Error sending photo {full_path} for route {route_id}: {e}")
        else:
            logging.warning(f"Photo file not found: {full_path} for route {route_id}")

    if sent_photos_count < len(photos) and len(photos) > 0:
        await callback.message.answer(t("photo_error", lang))
    elif len(photos) == 0:
        logging.info(f"No photos specified for route ID {route_id}.")

    desc = route.get("description", "")
    map_url = route.get("map_url", "")

    # Send the route details with an inline "Back to Routes" button
    # The ReplyKeyboard should already be hidden from process_interest.
    await callback.message.answer(
        f"<b>{route['title']}</b>\n\n{desc}\n\n📍 <a href='{map_url}'>Открыть в Google Maps</a>",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t("back_to_routes", lang), callback_data="back_to_route_list")]
            # This is the only "Back" button
        ])
    )

    await state.set_state(StateGroup.viewing_route_details)


@dp.callback_query(F.data == "back_from_routes_to_interest")
async def handle_back_from_routes_to_interest(callback: CallbackQuery, state: FSMContext):
    """
    Handles the 'Back to Interests' button from the inline route selection list.
    This is triggered from the list of inline routes, taking user back to interest selection.
    """
    await callback.answer()
    data = await state.get_data()
    lang = data.get("lang", "ru")

    # Re-display the ReplyKeyboard for interest selection
    interest_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=TRANSLATIONS["interests"][lang][0]),
             KeyboardButton(text=TRANSLATIONS["interests"][lang][1])],
            [KeyboardButton(text=TRANSLATIONS["interests"][lang][2])],
            [KeyboardButton(text=t("back", lang))]  # This ReplyKeyboard has a "Back" button to city
        ],
        resize_keyboard=True
    )
    await callback.message.answer(t("choose_interest", lang), reply_markup=interest_keyboard)
    await state.set_state(StateGroup.interest)


@dp.callback_query(F.data == "back_to_route_list")
async def handle_back_to_route_list(callback: CallbackQuery, state: FSMContext):
    """
    Handles 'Back to Routes' button after viewing a specific route.
    This takes the user back to the inline list of routes for the chosen city/interest.
    """
    await callback.answer()
    data = await state.get_data()
    lang = data.get("lang", "ru")

    current_city = data.get("city")
    current_interest = data.get("interest")

    if current_city and current_interest:
        routes = await get_routes_by_city_and_interest(current_city, current_interest, lang)
        if routes:
            inline_buttons = []
            for r in routes:
                inline_buttons.append([InlineKeyboardButton(text=r["title"], callback_data=f"route_{r['id']}")])
            inline_buttons.append([InlineKeyboardButton(text=t("back_to_interest_selection", lang),
                                                        callback_data="back_from_routes_to_interest")])  # Inline back to interest

            await callback.message.answer(
                t("choose_route", lang),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_buttons)
            )
            await state.set_state(StateGroup.route)
            return

    # Fallback if no routes found or data missing, go to interest selection with ReplyKeyboard
    interest_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=TRANSLATIONS["interests"][lang][0]),
             KeyboardButton(text=TRANSLATIONS["interests"][lang][1])],
            [KeyboardButton(text=TRANSLATIONS["interests"][lang][2])],
            [KeyboardButton(text=t("back", lang))]
        ],
        resize_keyboard=True
    )
    await callback.message.answer(t("choose_interest", lang), reply_markup=interest_keyboard)
    await state.set_state(StateGroup.interest)


@dp.message(
    F.text == TRANSLATIONS["back"]["ru"] or
    F.text == TRANSLATIONS["back"]["en"] or
    F.text == TRANSLATIONS["back"]["uz"]
)
async def universal_back(message: Message, state: FSMContext):
    """
    Handles the universal 'Back' button for ReplyKeyboards.
    This handler only applies when a ReplyKeyboardMarkup is currently active.
    """
    current_state = await state.get_state()
    data = await state.get_data()
    lang = data.get("lang", "ru")

    # This 'Back' button is part of the ReplyKeyboardMarkup,
    # so it should only be active when ReplyKeyboards are shown (language, city, interest states).

    if current_state == StateGroup.interest.state:
        # From interest selection (ReplyKeyboard active), go back to city selection
        await state.set_state(StateGroup.city)
        city_keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=city)] for city in TRANSLATIONS["cities"]] +
                     [[KeyboardButton(text=t("back", lang))]],
            resize_keyboard=True
        )
        await message.answer(t("choose_city", lang), reply_markup=city_keyboard)

    elif current_state == StateGroup.city.state:
        # From city selection (ReplyKeyboard active), go back to language selection (start)
        await start_command(message, state)
    else:
        # If 'back' is pressed from an unexpected state (e.g., viewing route details where ReplyKeyboard is removed)
        # or initial state, restart the flow and explicitly remove current keyboards.
        await message.answer(t("invalid_selection", lang), reply_markup=ReplyKeyboardRemove())
        await start_command(message, state)


# --- Main Bot Execution ---
async def main():
    """Starts the bot polling."""
    logging.info("Bot is starting...")
    await dp.start_polling(bot)
    logging.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())