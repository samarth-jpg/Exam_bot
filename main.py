import os
import json
import threading
from flask import Flask
import telebot

# Flask app for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Exam Question Bot is running on Render!"

# Load questions dataset
with open("questions.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

# Telegram bot setup
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Add BOT_TOKEN in Render environment
bot = telebot.TeleBot(BOT_TOKEN)

# /start and /help command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
    "👋 Welcome to Exam Question Bot!\n\n"
    "📚 Send me exam name + year (e.g., 'UPSC 2020') "
    "and I’ll fetch previous year questions for you."
    )

# Search handler
@bot.message_handler(func=lambda message: True)
def search_questions(message):
    query = message.text.lower()
    results = [q for q in QUESTIONS if q['exam'].lower() in query and q['year'] in query]

    if results:
        for q in results:
            bot.send_message(message.chat.id, f"📖 {q['exam']} {q['year']}:\n{q['question']}")
    else:
        bot.send_message(message.chat.id, "❌ No questions found. Try again (e.g., 'SSC 2019').")

# Run bot in background
def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    # Start Telegram bot in a separate thread
    threading.Thread(target=run_bot).start()

    # Run Flask app (needed for Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)