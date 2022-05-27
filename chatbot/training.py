import json
import random
import numpy as np

import spacy

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical


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
            print(token.lemma_)
            words.append(token.text)
            if token.text not in ignore_list:
                words_lemma.append(token.lemma_)
        documents.append((word_list, intent["class"]))
        if intent["class"] not in classes:
            classes.append(intent["class"])
print(documents)
print(classes)
print(words)
print(words_lemma)

words_lemma = sorted(set(words_lemma))
print(words_lemma)

training_data = []
training_labels = []

for document in documents:
    bag = [0] * len(words_lemma)
    word_patterns = document[0]
    print(word_patterns)
    word_list = nlp(word_patterns)
    word_patterns_lemma = []
    for token in word_list:
        word_patterns_lemma.append(token.lemma_)
    for index, word_lemma in enumerate(words_lemma):
        if word_lemma in word_patterns_lemma:
            bag[index] = bag[index] + 1
    bag = np.array(bag)
    training_labels.append(document[1])
    training_data.append(bag)
training_data = np.array(training_data)
training_labels = np.array(training_labels)
training_labels = to_categorical(training_labels,num_classes=4)
print(training_data)
print(training_labels)
print(len(words_lemma))
print(len(classes))


model = Sequential()
model.add(Dense(128, input_shape=(len(words_lemma),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64,activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(classes), activation="softmax"))

model.compile(loss="categorical_crossentropy",optimizer=SGD(lr=0.01,decay=1e-6,momentum=0.9,nesterov=True), metrics=['accuracy'])
#model.compile(loss="categorical_crossentropy",optimizer="adam", metrics=['accuracy'])


pretrained_model = model.fit(training_data, training_labels, epochs=200, batch_size=5, verbose=1)
model.save("chatbot.h5", pretrained_model)