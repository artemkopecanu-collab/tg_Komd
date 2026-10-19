import telebot
import requests
from telebot import types

# Твой токен
TOKEN = "8159204639:AAFlGQP51_CYNWNIXQN8nNq5-chDdYfqI7o"
bot = telebot.TeleBot(TOKEN)

# Функция, которая собирает данные погоды и курса
def get_weather_and_rate():
    # 1. Получаем курс валют
    try:
        url_curr = "https://open.er-api.com/v6/latest/KZT"
        res_curr = requests.get(url_curr).json()
        rate_rub = res_curr["rates"]["RUB"]
        tenge_to_rub = round(rate_rub, 4)
        rub_to_tenge = round(1 / rate_rub, 2)
        curr_text = f"💱 **Курс валют:**\n• 1 KZT = {tenge_to_rub} RUB\n• 1 RUB = {rub_to_tenge} KZT"
    except:
        curr_text = "💱 Не удалось получить курс валют."

    # 2. Получаем погоду (Алматы)
    try:
        url_weather = "https://api.open-meteo.com/v1/forecast?latitude=43.2567&longitude=76.9286&current=temperature_2m,apparent_temperature"
        res_weather = requests.get(url_weather).json()
        temp = res_weather["current"]["temperature_2m"]
        feels = res_weather["current"]["apparent_temperature"]
        weather_text = f"🌤 **Погода (Алматы):**\n• Температура: {temp}°C\n• Ощущается как: {feels}°C"
    except:
        weather_text = "🌤 Не удалось узнать погоду."

    # Собираем всё вместе
    return f"📊 **Твоя ежедневная сводка:**\n\n{curr_text}\n\n{weather_text}"

# Команда /start — приветствие и кнопка
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру с одной кнопкой
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📥 Получить сводку", callback_data="get_summary")
    markup.add(btn)
    
    bot.send_message(
        message.chat.id, 
        "Привет! Нажми на кнопку ниже, чтобы получить курс тенге и погоду в одно нажатие.",
        reply_markup=markup
    )

# Обработка нажатия на кнопку
@bot.callback_query_handler(func=lambda call: call.data == "get_summary")
def callback_query(call):
    # Убираем "часики" загрузки с кнопки
    bot.answer_callback_query(call.id)
    
    # Генерируем текст и отправляем пользователю
    summary_text = get_weather_and_rate()
    bot.send_message(call.message.chat.id, summary_text, parse_mode="Markdown")

# На случай, если напишут обычный текст
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Напиши /start, чтобы получить кнопку для сводки.")

print("Бот с кнопкой запущен и ждет...")
bot.infinity_polling()