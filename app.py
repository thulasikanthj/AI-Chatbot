from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

conversation = [{"role": "system", "content": "You are a helpful AI assistant. Answer in full sentences."}]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."})
    conversation.append({"role": "user", "content": user_message})
    if len(conversation) > 8:
        conversation.pop(1)
    prompt = "You are a helpful AI assistant. Answer in full sentences.\n\n"
    for msg in conversation:
        if msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        elif msg["role"] == "bot":
            prompt += f"Bot: {msg['content']}\n"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma:2b", "prompt": prompt, "stream": False, "max_tokens": 300},
            timeout=60
        )
        result = response.json()
        reply = result.get("response", "").strip()

        if not reply:
            reply = "Sorry, I couldn't generate a reply."

        conversation.append({"role": "bot", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
