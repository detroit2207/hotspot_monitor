from flask import Flask, jsonify

app = Flask(__name__)

# Dummy data: Map usernames to chat IDs
chat_id_map = {
    "ajay_coolguy": "7186421280",
    "nandakishore": "1234567890",
    "bala_tech": "1122334455"
}

@app.route('/get_chat_id/<username>', methods=['GET'])
def get_chat_id(username):
    chat_id = chat_id_map.get(username)
    if chat_id:
        return jsonify({"chat_id": chat_id})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
