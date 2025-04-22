from flask import Flask, request
import requests
import os
from processor import chatbot_response  # 🤖 chatbot-оос хариу авах

app = Flask(__name__)

# 🔐 Environment variables-оос авах
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge
        return 'Invalid verification token', 403

    elif request.method == 'POST':
        data = request.get_json()
        print("🔔 Message received:", data)

        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                if "message" in messaging_event:
                    message_text = messaging_event["message"].get("text", "")

                    # 🤖 Chatbot-р хариу боловсруулах
                    bot_reply = chatbot_response(message_text)
                    print("🔍 Predicted reply:", bot_reply)

                    # 💬 Хариу илгээх
                    send_message(sender_id, bot_reply)

        return 'EVENT_RECEIVED', 200

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    response = requests.post(url, params=params, headers=headers, json=data)
    print("📨 Sent message:", response.status_code, response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

