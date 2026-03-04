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

# ১. আপনার নতুন তথ্য
BOT_TOKEN = "8458877465:AAEZoRhw9O9X1Xv6Ivlc__sBmvPhUniSKbc"
GEMINI_API_KEY = "AIzaSyCMnYK3IQXWLtx2orTb9sb2zP6xAnkqndI" # আপনার নতুন কি এখানে বসানো হয়েছে
ADMIN_ID = 7468233796 

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
BANNER_URL = "https://i.ibb.co/vzVfVfV/islamic-cyber-banner.jpg"

def ask_gemini(user_text):
    # v1beta ব্যবহার করা হয়েছে দ্রুত রেসপন্সের জন্য
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    system_instruction = (
        "You are an Advanced Islamic AI Scholar named 'An-Noor Sentinel'. "
        "Provide authentic knowledge based on Quran & Sahih Hadith in Bangla. "
        "Keep answers concise and clear."
    )

    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nUser: {user_text}"}]}]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Error: {e}")
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

if __name__ == "__main__":
    keep_alive() 
    print("Bot is Alive and Hosting...")
    bot.infinity_polling()
