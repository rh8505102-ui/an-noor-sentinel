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

# ১. আপনার তথ্য আপডেট করা হয়েছে
BOT_TOKEN = "8458877465:AAEZoRhw9O9X1Xv6Ivlc__sBmvPhUniSKbc"
GEMINI_API_KEY = "AIzaSyDWiVbtYqeuxGW8ZnWIHN73qd17AIcL3eM" # নতুন কি এখানে বসানো হয়েছে
ADMIN_ID = 7468233796 

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
BANNER_URL = "https://i.ibb.co/vzVfVfV/islamic-cyber-banner.jpg"

def ask_gemini(user_text):
    # গুগলের লেটেস্ট এন্ডপয়েন্ট ব্যবহার করা হয়েছে
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    system_instruction = (
        "You are An-Noor Sentinel, an Advanced Islamic AI Scholar. "
        "Provide authentic knowledge based on Quran & Sahih Hadith in Bangla."
    )

    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nUser: {user_text}"}]}]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "⚠️ গুগল সার্ভার থেকে কোনো তথ্য পাওয়া যায়নি। কি-টি আবার চেক করুন।"
    except:
        return "⚠️ বর্তমানে সার্ভার ব্যস্ত। অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।"

# কিবোর্ড মেনু
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🕌 নামাজ শিক্ষা (A-Z)", "🚿 ওযু ও পবিত্রতা", "🌙 সাহাবীদের বীরত্ব", "📜 কুরআন ও হাদিস", "⚖️ হালাল-হারাম বিধান", "🤲 দৈনন্দিন দোয়া", "🔗 বট শেয়ার করুন")
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    welcome_msg = "আসসালামু আলাইকুম! আমি **An-Noor Sentinel**। আপনার দ্বীনি জিজ্ঞাসার সমাধানে আমি প্রস্তুত।"
    try:
        bot.send_photo(message.chat.id, BANNER_URL, caption=welcome_msg, reply_markup=main_menu())
    except:
        bot.send_message(message.chat.id, welcome_msg, reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def handle(message):
    if message.text == "🔗 বট শেয়ার করুন":
        bot.reply_to(message, f"শেয়ার করুন: https://t.me/{bot.get_me().username}")
        return
    
    bot.send_chat_action(message.chat.id, "typing")
    reply = ask_gemini(message.text)
    bot.reply_to(message, reply)

if __name__ == "__main__":
    keep_alive() 
    print("Bot is Alive...")
    bot.infinity_polling()
