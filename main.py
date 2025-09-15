import os
import telebot

# Get your bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Start/help command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hello! Your bot is live and working!")

# Echo handler (replies back same message)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

print("🤖 Bot is running...")
bot.infinity_polling()
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Your bot is running successfully on Render!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render gives a PORT env variable
    app.run(host="0.0.0.0", port=port)