from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

BOT_TOKEN = "7715743565:AAH_dKW6dOMWdGb_7t4_INxDT-LToZt6gsQ"

BACKEND_REGISTER_URL = "https://hotspot-monitor.onrender.com/register"

def start(update, context):
    username = update.message.text.split(" ")[1] if len(update.message.text.split()) > 1 else None
    if not username:
        update.message.reply_text("Please restart the bot with your username like this:\n/start yourusername")
        return

    chat_id = update.message.chat_id
    data = {
        "username": username,
        "chat_id": str(chat_id)
    }
    try:
        requests.post(BACKEND_REGISTER_URL, json=data)
        update.message.reply_text("✅ Registered successfully!\nYou’ll now receive notifications.")
    except:
        update.message.reply_text("❌ Failed to register. Try again later.")

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
updater.start_polling()
