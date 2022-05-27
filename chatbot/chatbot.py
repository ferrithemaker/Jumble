import random
import json

import numpy as np
import spacy
from tensorflow.keras.models import load_model

nlp = spacy.load("ca_core_news_sm")

intents = json.loads(open("chatbotmodel.json").read())

words = []
words_lemma = []
classes = []
documents = []
ignore_list = ['?','¿',':',',','.','i','o','!','¡']

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        word_list = nlp(pattern)
        for token in word_list:
            #print(token.lemma_)
            words.append(token.text)
            if token.text not in ignore_list:
                words_lemma.append(token.lemma_)
        documents.append((word_list, intent["class"]))
        if intent["class"] not in classes:
            classes.append(intent["class"])

words_lemma = sorted(set(words_lemma))
model = load_model("chatbot.h5")

def clean_up_sentence(sentence):
    list_of_words = []
    sentence_word_list = nlp(sentence)
    for token in sentence_word_list:
        if token.text not in ignore_list:
            list_of_words.append(token.lemma_)
    return list_of_words

def bag_of_words(sentence):
    sentence_word_list = clean_up_sentence(sentence)
    bag = [0] * len(words_lemma)
    for w in sentence_word_list:
        for index, word_lemma in enumerate(words_lemma):
            if word_lemma == w:
                bag[index] = bag[index] + 1
    return bag

def predict_class(sentence):
    bag = bag_of_words(sentence)
    res = model.predict(np.array([bag]), verbose=0)
    return np.argmax(res)

def get_response(predicted_class):
    for intent in intents["intents"]:
        if intent["class"] == predicted_class:
            response = random.choice(intent["responses"])
    return response


while True:
    sentence = input("> ")
    bag = bag_of_words(sentence)
    predicted_class = predict_class(sentence)
    print(get_response(predicted_class))