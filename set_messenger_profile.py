import requests
import json

# 🔁 Энд туршилтын эсвэл ЖИНХЭНЭ Page access token-оо тавь
PAGE_ACCESS_TOKEN = 'ТАНЫ_PAGE_ACCESS_TOKEN'

url = f"https://graph.facebook.com/v18.0/me/messenger_profile?access_token={PAGE_ACCESS_TOKEN}"

payload = {
    "get_started": {
        "payload": "GET_STARTED"
    },
    "greeting": [
        {
            "locale": "default",
            "text": "Сайн байна уу! Би ШМТДС-ийн албан ёсны чатбот. Юуны талаар мэдээлэл авахыг хүсэж байна вэ?"
        }
    ],
    "persistent_menu": [
        {
            "locale": "default",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "🎓 Сургалтын алба",
                    "payload": "CONTACT_OFFICE"
                },
                {
                    "type": "postback",
                    "title": "📚 Элсэлтийн мэдээлэл",
                    "payload": "ADMISSION_INFO"
                },
                {
                    "type": "postback",
                    "title": "🤖 Чатботтой ярих",
                    "payload": "TALK_TO_BOT"
                }
            ]
        }
    ]
}

headers = {
    "Content-Type": "application/json"
}

res = requests.post(url, headers=headers, json=payload)

print("✅ Хариу:", res.status_code)
print(res.json())
