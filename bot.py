from flask import Flask, request
import telebot
import os
print("BOT STARTED")
print("TOKEN from env:", os.environ.get('BOT_TOKEN')[:10] + "..." if os.environ.get('BOT_TOKEN') else "TOKEN IS NONE!!!")
print("WEBHOOK_PATH:", WEBHOOK_PATH)

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    raise ValueError("BOT_TOKEN not set!")

bot = telebot.TeleBot(TOKEN)

WEBHOOK_PATH = f'/{TOKEN}'

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Сәлем! Мен Әбділданың жаңа боты. Жазып көр!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        text = message.text or '(ештеңе жазбағансың)'
        bot.reply_to(message, f"Сен жаздың: {text} ✅")
    except Exception as e:
        bot.reply_to(message, "Қате шықты, кешір 😔")

@app.route('/', methods=['GET'])
def home():
    return "Бот тірі! ✅", 200

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Invalid', 403

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
