UPDATE routes
SET schedule_json = '
[
  {
    "time": "09:00",
    "activity_ru": "Выезд из Ташкента",
    "activity_en": "Departure from Tashkent",
    "activity_uz": "Toshkentdan chiqish"
  },
  {
    "time": "11:00",
    "activity_ru": "Подъём на канатке в Чимгане",
    "activity_en": "Cable car ride in Chimgan",
    "activity_uz": "Chimyonda arqon yo‘lga chiqish"
  },
  {
    "time": "13:00",
    "activity_ru": "Обед в кафе у озера",
    "activity_en": "Lunch near the lake",
    "activity_uz": "Ko‘l yonidagi kafeda tushlik"
  },
  {
    "time": "17:00",
    "activity_ru": "Возвращение в Ташкент",
    "activity_en": "Return to Tashkent",
    "activity_uz": "Toshkentga qaytish"
  }
]'
WHERE city = 'tashkent' AND interest = 'nature' AND title = '🏞️ Чарвак и Чимган';
