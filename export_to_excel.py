from pymongo import MongoClient
import pandas as pd

# MongoDB-т холбогдох
client = MongoClient("mongodb://localhost:27017/")
db = client.chatbot_db
questions = db.questions

# Mongo-оос бүх асуултыг авна
data = list(questions.find({}, {"_id": 0}))  # _id-г үл оролцуулна
df = pd.DataFrame(data)

# Excel файл болгон хадгалах
df.to_excel("chat_logs.xlsx", index=False)
