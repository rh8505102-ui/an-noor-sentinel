import telebot
import requests
from telebot import types
import time
from flask import Flask
from threading import Thread

# --- Flask Server for 24/7 Hosting ---
app = Flask('')

@app.route('/')
def home():
    return "An-Noor Sentinel is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Configuration ---
BOT_TOKEN = "8458877465:AAEZoRhw9O9X1Xv6Ivlc__sBmvPhUniSKbc"
GEMINI_API_KEY = "AIzaSyCMnYK3IQXWLtx2orTb9sb2zP6xAnkqndI"
ADMIN_ID = 7468233796 

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
BANNER_URL = "https://i.ibb.co/vzVfVfV/islamic-cyber-banner.jpg"

def ask_gemini(user_text):
    # Try both v1 and v1beta for maximum compatibility
    endpoints = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    ]
    
    system_instruction = (
        "You are 'An-Noor Sentinel', an Advanced Islamic AI Scholar. "
        "Answer strictly in Bangla using Quran and Sahih Hadith."
    )

    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nUser: {user_text}"}]}]
    }

    for url in endpoints:
        try:
            response = requests.post(url, json=payload, timeout=20)
            data = response.json()
            if 'candidates' in data:
                return data['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
            
    return "⚠️ দুঃখিত, আমার ইসলামিক নলেজ ডাটাবেস এই মুহূর্তে সাড়া দিচ্ছে না। অনুগ্রহ করে ৫ মিনিট পর আবার চেষ্টা করুন।"

# --- Menu ---
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
