from flask import Flask, request, jsonify

app = Flask(__name__)
user_db = {}  # Temporary in-memory storage

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.json
    if 'message' in data:
        username = data["message"]["from"].get("username", "unknown_user")
        chat_id = data["message"]["chat"]["id"]
        user_db[username] = chat_id
        print(f"Saved {username} -> {chat_id}")
    return "OK"

@app.route("/get_chat_id/<username>", methods=["GET"])
def get_chat_id(username):
    chat_id = user_db.get(username)
    return jsonify({"chat_id": chat_id}) if chat_id else ("User not found", 404)

@app.route("/", methods=["GET"])
def home():
    return "Bot is alive!"
