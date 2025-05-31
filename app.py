from flask import Flask, jsonify
from telegram.ext import Updater, CommandHandler
import threading
import requests

app = Flask(__name__)

# Store username -> chat_id
user_data = {}

# Your bot token
BOT_TOKEN = "7715743565:AAH_dKW6dOMWdGb_7t4_INxDT-LToZt6gsQ"


def start(update, context):
    try:
        if context.args:
            username = context.args[0]
            chat_id = update.effective_chat.id
            user_data[username] = chat_id
            update.message.reply_text(f"✅ Registered as {username}!\nYou’ll now get alerts.")
        else:
            update.message.reply_text("❌ Username missing! Use /start your_username")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def get_chat_id(username):
    return user_data.get(username)

@app.route("/get_chat_id/<username>", methods=["GET"])
def handle_get_chat_id(username):
    chat_id = get_chat_id(username)
    if chat_id:
        return jsonify({"chat_id": chat_id})
    else:
        return jsonify({"error": "User not found"}), 404

def run_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start, pass_args=True))
    updater.start_polling()
    updater.idle()

# Run bot in separate thread
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
