from flask import request

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    chat_id = data.get("chat_id")

    if not username or not chat_id:
        return jsonify({"error": "Missing username or chat_id"}), 400

    chat_id_map[username] = chat_id

    # Optional: Save to file if you're using JSON storage
    with open("chat_ids.json", "w") as f:
        json.dump(chat_id_map, f)

    return jsonify({"message": "User registered successfully."})
