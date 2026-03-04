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
