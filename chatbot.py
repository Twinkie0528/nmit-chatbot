import nltk
nltk.download('punkt')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping

import numpy as np
import json
import pickle
import random
import argparse
import re
from collections import Counter

# -----------------------------
# Argument parser for CLI args
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--epochs", type=int, default=300, help="Number of training epochs")
parser.add_argument("--batch_size", type=int, default=8, help="Training batch size")
args = parser.parse_args()

# -----------------------------
# Preprocessing tools
# -----------------------------
lemmatizer = WordNetLemmatizer()
ignore_words = ['?', '!', '.', ',']

def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower()

# -----------------------------
# Load intents JSON
# -----------------------------
with open('job_intents.json', encoding='utf-8') as f:
    intents = json.load(f)

words = []
classes = []
documents = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        cleaned = clean_text(pattern)
        w = nltk.word_tokenize(cleaned)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

print(f"\n📄 {len(documents)} documents")
print(f"🏷️  {len(classes)} classes: {classes}")
print(f"🔠 {len(words)} unique lemmatized words")

print("\nClass distribution:")
print(Counter([doc[1] for doc in documents]))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# -----------------------------
# Create training data
# -----------------------------
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = [lemmatizer.lemmatize(w.lower()) for w in doc[0]]
    bag = [1 if w in pattern_words else 0 for w in words]

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)
train_x = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

# -----------------------------
# Build model
# -----------------------------
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# -----------------------------
# Train model
# -----------------------------
early_stop = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
hist = model.fit(train_x, train_y, epochs=args.epochs, batch_size=args.batch_size, verbose=1, callbacks=[early_stop])

# Save model and training history
model.save('chatbot_model.h5')
pickle.dump(hist.history, open("history.pkl", "wb"))

print("\n✅ Model successfully trained and saved as chatbot_model.h5")
