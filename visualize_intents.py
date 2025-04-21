from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

# MongoDB-т холбогдох
client = MongoClient("mongodb://localhost:27017/")
db = client.chatbot_db
questions = db.questions

# Бүх асуултыг авна
data = list(questions.find({}, {"_id": 0}))
df = pd.DataFrame(data)

# Intent-ээр тоолох
summary = df["intent"].value_counts().reset_index()
summary.columns = ["intent", "total"]

# -----------------------------
# 📊 Bar Chart: Intent-үүдийн тоо
# -----------------------------
plt.figure(figsize=(10, 6))
plt.bar(summary["intent"], summary["total"], color='skyblue')
plt.title("Intent-үүдийн давтамж")
plt.xlabel("Intent")
plt.ylabel("Нийт асуулт")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("intent_chart.png")
plt.show()

# -----------------------------
# 🥧 Pie Chart: Intent-үүдийн харьцаа
# -----------------------------
plt.figure(figsize=(8, 8))
plt.pie(summary["total"], labels=summary["intent"], autopct="%1.1f%%", startangle=140)
plt.title("Intent-үүдийн харьцаа (%)")
plt.tight_layout()
plt.savefig("intent_pie.png")
plt.show()
