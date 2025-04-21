import csv
from pymongo import MongoClient

# MongoDB-т холбогдох
client = MongoClient("mongodb://localhost:27017/")
db = client.chatbot_db
questions = db.questions

# CSV файл үүсгэх
with open("chat_logs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["question", "intent", "timestamp"])  # Header

    for q in questions.find():
        writer.writerow([
            q.get("question", ""),
            q.get("intent", ""),
            q.get("timestamp", "")
        ])
