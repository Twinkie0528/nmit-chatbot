import nltk
import os
import pickle
import numpy as np
import json
import random

from keras.models import load_model
from nltk.tokenize import wordpunct_tokenize  # 🆕
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient
from datetime import datetime

# ✅ nltk_data path-уудыг зааж өгнө (punkt, wordnet аль аль нь)
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data", "corpora"))

# 🧹 Лемматайзер
lemmatizer = WordNetLemmatizer()

# 💾 MongoDB холболт
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client.chatbot_db
    questions = db.questions
except:
    client = None
    questions = None

def log_user_question(user_input, intent=None):
    if questions:
        questions.insert_one({
            "question": user_input,
            "intent": intent,
            "timestamp": datetime.utcnow()
        })

# 🧠 Загвар болон өгөгдөл ачааллах
model = load_model("chatbot_model.h5")
intents = json.loads(open("job_intents.json", encoding="utf-8").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

# 🧹 Текст цэвэрлэх
def clean_up_sentence(sentence):
    sentence_words = wordpunct_tokenize(sentence)  # 🆕 punkt биш, wordpunct ашиглаж байна
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# 🧠 Bag of Words
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"📌 Found in bag: {w}")
    return np.array(bag)

# 🔍 Интент таамаглах
def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.4
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    print("🔎 Prediction Probabilities:", results)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

# 💬 JSON-оос хариу авах
def get_json_response(ints, intents_json):
    tag = ints[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])

# 🧠 Chatbot хариу
def chatbot_response(msg):
    print(f"🗣️ User Message: {msg}")
    ints = predict_class(msg, model)
    print(f"🧠 Intent Prediction: {ints}")

    if ints:
        prob = float(ints[0]["probability"])
        if prob > 0.85:
            intent = ints[0]["intent"]
            log_user_question(msg, intent)
            return get_json_response(ints, intents)

    log_user_question(msg, "unknown")
    return "🤖 Уучлаарай, таны асуултад хариулах боломжгүй байна. Та өөрөөр дахин оролдоорой."
