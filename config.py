import os
from dotenv import load_dotenv

# Загружаем переменные из .env (локально)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Установите его в .env или переменные окружения.")

