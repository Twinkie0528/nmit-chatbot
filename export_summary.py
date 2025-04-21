from pymongo import MongoClient
import pandas as pd

# MongoDB-т холбогдох
client = MongoClient("mongodb://localhost:27017/")
db = client.chatbot_db
questions = db.questions

# Бүх өгөгдлийг авах
data = list(questions.find({}, {"_id": 0}))
df = pd.DataFrame(data)

# Intent-үүдийг тоолох
summary = df["intent"].value_counts().reset_index()
summary.columns = ["intent", "total"]

# Excel файл болгон хадгалах
summary.to_excel("intent_summary.xlsx", index=False)
