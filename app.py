from flask import Flask, jsonify
from telegram.ext import Updater, CommandHandler
import threading
import json
import os

app = Flask(__name__)
BOT_TOKEN = "7715743565:AAH_dKW6dOMWdGb_7t4_INxDT-LToZt6gsQ"

DATA_FILE = "users.json"

# --- Load from file ---
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# --- Save to file ---
def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

user_data = load_users()

def start(update, context):
    try:
        if context.args:
            username = context.args[0].strip().lower()  # normalize username
            chat_id = update.effective_chat.id

            # Reload user_data fresh to avoid race conditions
            current_users = load_users()

            if username in current_users:
                update.message.reply_text(f"❌ Username '{username}' is already taken. Please choose another.")
            else:
                current_users[username] = chat_id
                save_users(current_users)
                update.message.reply_text(f"✅ Registered as {username}!")
        else:
            update.message.reply_text("❌ Username missing! Use /start your_username")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

@app.route("/get_chat_id/<username>", methods=["GET"])
def handle_get_chat_id(username):
    username = username.strip().lower()  # normalize username lookup
    user_data = load_users()  # Always read latest from file
    chat_id = user_data.get(username)
    if chat_id:
        return jsonify({"chat_id": chat_id})
    else:
        return jsonify({"error": "User not found"}), 404

def run_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start, pass_args=True))
    updater.start_polling()
    # No updater.idle()


# Run bot in a separate thread
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
