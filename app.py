from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "dh_keys.json"
MESSAGE_FILE = "messages.json"

# Function to load JSON data safely, ensuring correct data type
def load_data(filename, expected_type):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                data = json.load(file)
                if not isinstance(data, expected_type):
                    return expected_type()  # Return empty list or dict if data type is incorrect
                return data
            except json.JSONDecodeError:
                return expected_type()
    return expected_type()  # Always return expected data type

# Function to save JSON data
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file)

# Load stored keys and messages at startup
keys = load_data(DATA_FILE, dict)  # Ensure keys is always a dictionary
messages = load_data(MESSAGE_FILE, list)  # Ensure messages is always a list

@app.route("/")
def index():
    return render_template("index1.html")

# Store user's public key
@app.route("/submit_key", methods=["POST"])
def submit_key():
    data = request.get_json()
    user_id = data.get("user_id")
    public_key = data.get("public_key")

    if user_id and public_key:
        keys[user_id] = public_key  # Store public key
        save_data(DATA_FILE, keys)  # Save keys
        return jsonify({"status": "success"}), 200

    return jsonify({"status": "error"}), 400

# Retrieve all stored public keys
@app.route("/get_keys", methods=["GET"])
def get_keys():
    return jsonify(keys)

# Retrieve all stored encrypted messages
@app.route("/get_messages", methods=["GET"])
def get_messages():
    return jsonify(messages)

# Store encrypted messages
@app.route("/store_message", methods=["POST"])
def store_message():
    global messages  # Ensure we're using the global list
    data = request.get_json()
    encrypted_text = data.get("encrypted_message")

    if encrypted_text:
        if not isinstance(messages, list):  # Ensure messages is a list
            messages = []
        messages.append(encrypted_text)
        save_data(MESSAGE_FILE, messages)
        return jsonify({"status": "success"}), 200

    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=55555)
