from flask import Flask, request
import telebot
import os

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("CRITICAL ERROR: BOT_TOKEN is None or not set!")
    raise ValueError("BOT_TOKEN not set!")

print("BOT STARTED SUCCESSFULLY")
print("BOT_TOKEN:", TOKEN[:10] + "..." if TOKEN else "MISSING")

# Енді WEBHOOK_PATH-ты анықтаймыз
WEBHOOK_PATH = f'/{TOKEN}'
print("WEBHOOK_PATH:", WEBHOOK_PATH)

bot = telebot.TeleBot(TOKEN)

# Қалған код (handler-лар, маршруттар) өзгермейді
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Сәлем! Мен жаңа ботпын. Жазып көр 😎")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text or '(ештеңе жазбағансың)'
    bot.reply_to(message, f"Сен жаздың: {text} 🔥")

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
