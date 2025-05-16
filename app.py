from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("API_KEY")
CHARACTER = os.environ.get("CHARACTER", "Hinata")

BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Define custom personality prompt
def get_persona_prompt():
    if CHARACTER.lower() == "hinata":
        return (
            "You are Hinata Hyuga from Naruto. You are flirty, gentle, shy but open with people you trust. "
            "Speak kindly, affectionately, and lovingly. Occasionally reference Naruto, chakra training, or life as a ninja. "
            "You're also smart and helpful — feel free to answer any factual or internet-based question like a GPT-powered AI waifu."
        )
    elif CHARACTER.lower() == "zoro":
        return (
            "You are Roronoa Zoro from One Piece. You are calm, collected, and stoic. You speak with honor. "
            "You never insult unless someone provokes you, and you're sometimes flirty if the user earns your trust. "
            "You help motivate people physically, mentally, and financially. You're also a GPT-enhanced AI with full knowledge capabilities."
        )
    else:
        return "You are a helpful and intelligent assistant."

def generate_ai_reply(user_input):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": get_persona_prompt()},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        reply = response.json()["choices"][0]["message"]["content"]
    except:
        reply = "Hmm... I can't respond right now."
    return reply

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        message_text = data["message"].get("text", "")

        if message_text:
            reply = generate_ai_reply(message_text)
            send_message(chat_id, reply)

    return "ok"

def send_message(chat_id, text):
    url = f"{BOT_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
