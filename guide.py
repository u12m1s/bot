import openai
from config import OPENAI_API_KEY
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_plan(city, days, interest, lang):
    city = city.lower()
    days = str(days).strip()
    interest = interest.lower()

    # Пример: Самарканд — 1 день — история
    if city in ["самарканд", "samarqand", "samarkand"] and days == "1":
        if interest in ["история", "tarix", "history"]:
            if lang == "ru":
                return (
                    "📍 <b>Самарканд — 1 день (История)</b>\n"
                    "• 🕌 Регистан\n"
                    "• 🕋 Гур Эмир\n"
                    "• 🏛️ Шахи-Зинда\n"
                    "• 🕌 Биби-Ханум\n\n"
                    "🗺️ <a href='https://goo.gl/maps/Bzgh4AjQ4DFGkC3b7'>Открыть карту</a>"
                )
            elif lang == "uz":
                return (
                    "📍 <b>Samarqand — 1 kun (Tarix)</b>\n"
                    "• 🕌 Registon\n"
                    "• 🕋 Amir Temur maqbarasi\n"
                    "• 🏛️ Shohi Zinda\n"
                    "• 🕌 Bibi Xonim\n\n"
                    "🗺️ <a href='https://goo.gl/maps/Bzgh4AjQ4DFGkC3b7'>Xaritani ochish</a>"
                )
            elif lang == "en":
                return (
                    "📍 <b>Samarkand — 1 Day (History)</b>\n"
                    "• 🕌 <b>Registan</b>\n"
                    "• 🕋 Gur Emir\n"
                    "• 🏛️ Shah-i-Zinda\n"
                    "• 🕌 Bibi-Khanym Mosque\n\n"
                    "🗺️ <a href='https://goo.gl/maps/Bzgh4AjQ4DFGkC3b7'>Open in Google Maps</a>"
                )

    return {
        "ru": "😕 Маршрут пока недоступен. Попробуй другие параметры.",
        "uz": "😕 Yo‘nalish mavjud emas. Iltimos, boshqa variantni tanlang.",
        "en": "😕 Route is not available yet. Try different options."
    }.get(lang, "Маршрут не найден.")
