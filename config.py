import os
from dotenv import load_dotenv

# Загружаем переменные из .env, если они есть
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Установите его в переменные окружения или в .env файл.")

