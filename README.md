import telebot
import requests
from telebot import types
import time
from flask import Flask
from threading import Thread

# --- Render-এ বটকে জাগিয়ে রাখার জন্য Flask সার্ভার ---
app = Flask('')

@app.route('/')
def home():
    return "An-Noor Sentinel is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------------------------

# ১. আপনার তথ্য (বট টোকেন ও এপিআই কি)
BOT_TOKEN = "8458877465:AAEZoRhw9O9X1Xv6Ivlc__sBmvPhUniSKbc"
GEMINI_API_KEY = "AIzaSyDu2Fdieybyr-LDAcE-2miO_q1xgAEiFak"
ADMIN_ID = 7468233796 

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
BANNER_URL = "https://i.ibb.co/vzVfVfV/islamic-cyber-banner.jpg"

def ask_gemini(user_text):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    system_instruction = (
        "You are an Advanced Islamic AI Scholar. Provide authentic knowledge "
        "based on Quran & Sahih Hadith in Bangla."
    )

    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nUser: {user_text}"}]}]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except:
        return "⚠️ বর্তমানে সার্ভার ব্যস্ত। অনুগ্রহ করে ইস্তিগফার পড়ুন এবং কিছুক্ষণ পর চেষ্টা করুন।"

# কিবোর্ড মেনু
def main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🕌 নামাজ শিক্ষা (A-Z)", "🚿 ওযু ও পবিত্রতা", "🌙 সাহাবীদের বীরত্ব", "📜 কুরআন ও হাদিস", "⚖️ হালাল-হারাম বিধান", "🤲 দৈনন্দিন দোয়া", "🔗 বট শেয়ার করুন")
    if user_id == ADMIN_ID:
        markup.add("⚡ অ্যাডমিন প্যানেল")
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    welcome_msg = "আসসালামু আলাইকুম! আমি **An-Noor Sentinel**। আপনার ইসলামিক জিজ্ঞাসার সমাধানে আমি প্রস্তুত।"
    try:
        bot.send_photo(message.chat.id, BANNER_URL, caption=welcome_msg, reply_markup=main_menu(message.from_user.id))
    except:
        bot.send_message(message.chat.id, welcome_msg, reply_markup=main_menu(message.from_user.id))

@bot.message_handler(func=lambda m: True)
def handle(message):
    if message.text == "🔗 বট শেয়ার করুন":
        bot.reply_to(message, f"শেয়ার করুন: https://t.me/{bot.get_me().username}")
        return
    
    bot.send_chat_action(message.chat.id, "typing")
    reply = ask_gemini(message.text)
    
    if len(reply) > 4000:
        for i in range(0, len(reply), 4000):
            bot.send_message(message.chat.id, reply[i:i+4000])
            time.sleep(1)
    else:
        bot.reply_to(message, reply)

# মেইন ফাংশন
if __name__ == "__main__":
    keep_alive() # Flask সার্ভার চালু হবে
    print("Bot is Alive and Hosting...")
    bot.infinity_polling() # বট কমান্ড শোনা শুরু করবে
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_photo(message.chat.id, BANNER_URL, caption="আসসালামু আলাইকুম! আমি আপনার **Islamic AI Assistant**।", reply_markup=main_menu(message.from_user.id))

@bot.message_handler(func=lambda m: True)
def handle(message):
    if message.text == "🔗 বট শেয়ার করুন":
        bot.reply_to(message, f"শেয়ার করুন: https://t.me/{(bot.get_me()).username}")
        return
    bot.send_chat_action(message.chat.id, "typing")
    reply = ask_gemini(message.text)
    if len(reply) > 4000:
        for i in range(0, len(reply), 4000):
            bot.send_message(message.chat.id, reply[i:i+4000])
            time.sleep(1)
    else: bot.reply_to(message, reply)

# --- নতুন ২ লাইন (সার্ভার স্টার্ট করার জন্য) ---
def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive() # সার্ভার চালু হবে
    print("Bot is Alive and Hosting...")
    bot.infinity_polling() # বট চালু হবে
