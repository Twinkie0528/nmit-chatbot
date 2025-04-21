from pymongo import MongoClient
import pandas as pd

# MongoDB-т холбогдох
client = MongoClient("mongodb://localhost:27017/")
db = client.chatbot_db
questions = db.questions

# Зөвхөн unknown intent-тай бичлэгүүдийг авах
data = list(questions.find({"intent": "unknown"}, {"_id": 0}))
df = pd.DataFrame(data)

# Excel файл болгон хадгалах
df.to_excel("unknown_questions.xlsx", index=False)

print(f"Нийт unknown intent-тай {len(data)} асуулт олдлоо.")
