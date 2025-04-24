from flask import Flask, request
import requests
import os
import nltk
from processor import chatbot_response

# ✅ NLTK tokenizer татах
nltk.download('punkt')

app = Flask(__name__)

# 🔐 Орчны хувьсагч (Render дээр ажиллана)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mini_token")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

# ✅ Локал тест бол шууд утга өгөх
if not PAGE_ACCESS_TOKEN:
    print("⚠️ Render-ийн PAGE_ACCESS_TOKEN олдсонгүй. Локал тест дээр байна гэж үзэж байна.")
    PAGE_ACCESS_TOKEN = "EAAaq5h6ecjQBOw3jZCkNtX5ZAJGPUtJqTDfWvnBTnkdOGop0kABufp2XL4DhJMIAcKNChZBQhZBneAFrlN7HvZAzUwJMaipq6pKOnOk9t3fiASRGSUsrPjqrlhFQMTWaBtY8Q4NTU0ZB27LT1AZBmbIeCJAfKlM3RCGCAyZBuV4W5Mn7997Mxt8l03TBfPczVwUWiwZDZD"  # 👉 Токеныг энд тавина уу

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            print("✅ VERIFY_TOKEN баталгаажлаа.")
            return challenge
        print("❌ VERIFY_TOKEN буруу байна.")
        return 'Invalid verification token', 403

    elif request.method == 'POST':
        data = request.get_json()
        print("🔔 Message received:", data)

        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                if "message" in messaging_event:
                    message_text = messaging_event["message"].get("text", "")
                    print(f"🗣️ User Message: {message_text}")

                    try:
                        bot_reply = chatbot_response(message_text)
                    except Exception as e:
                        print("❌ chatbot_response алдаа:", str(e))
                        bot_reply = "🤖 Уучлаарай, одоогоор хариу өгөх боломжгүй байна."

                    print(f"🤖 Bot Reply: {bot_reply}")
                    send_message(sender_id, bot_reply)

        return 'EVENT_RECEIVED', 200

def send_message(recipient_id, message_text):
    if not PAGE_ACCESS_TOKEN:
        print("❌ PAGE_ACCESS_TOKEN байхгүй тул хариу явуулах боломжгүй.")
        return

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
