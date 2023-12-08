import json
import pickle
import random

import keras
import nltk
import numpy as np
import tensorflow
import yaml
from matplotlib import pyplot
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy


def ParseData(asked=True):
    with open("DemoCollection.yaml") as yamlFile:
        YAML = yaml.safe_load(yamlFile)
    xlis = []
    ylis = []
    for cycle in YAML.get("v2"):
        title = cycle.get("dataType")
        for valueslist in cycle.get("data"):
            for values in valueslist.get("summary"):
                x = values.get("resource")
                xlis.append(x)
                if asked == False:
                    try:
                        y = values.get("status")[1].get("count")
                        ylis.append(y)
                    except:
                        pass
                else:
                    y = values.get("status")[0].get("count")
                    ylis.append(y)
    return xlis, ylis


def lineChart(Ask: bool):
    pyplot.cla()
    x, y = ParseData(Ask)
    pyplot.plot(np.array(x), np.array(y))
    pyplot.xticks(rotation=90)
    pyplot.pause(10)


def barChart(Ask):
    pyplot.cla()
    x, y = ParseData(Ask)
    pyplot.xticks(rotation=90)
    pyplot.bar(np.array(x), np.array(y))
    pyplot.pause(10)


def pieChart(Ask):
    pyplot.cla()
    x, y = ParseData(Ask)
    pyplot.pie(y, labels=x)
    pyplot.pause(10)


def Histogram():
    x, y = ParseData()
    pyplot.xticks(rotation=90)
    pyplot.hist(x)
    pyplot.pause(10)


def All(Ask):
    Histogram()
    lineChart(Ask)
    barChart(Ask)
    pieChart(Ask)


with open("BaseClassifier.json") as file:
    data = json.load(file)

try:
    with open("BaseClassifier.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("BaseClassifier.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

model = keras.Sequential(
    [
        keras.layers.Dense(training.shape[1], input_dim=training.shape[1]),
        keras.layers.Dense(100, activation="relu"),
        keras.layers.Dense(100, activation="relu"),
        keras.layers.Dense(output.shape[1], activation="softmax"),
    ]
)
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",  # sparse_categorical_crossentropy
    metrics=["accuracy"],
)

try:
    model.load("model.tflearn")
except:
    print(training.shape)
    print(output.shape)
    model.fit(training, output, epochs=1000, batch_size=8)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def chat():
    print("Start talking with the bot (type quit to stop)!")
    # textAnimation("Start talking with the bot (type quit to stop)!")
    while True:
        responses = []
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        input_tensor = [bag_of_words(inp, words)]
        input_tensor = tensorflow.reshape(input_tensor, shape=(1, training.shape[1]))
        results = model.predict(input_tensor)
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]

        ans = random.choice(responses)

        if "Line Chart" in ans:
            lineChart(True)
        if "Pie Chart" in ans:
            pieChart(True)
        if "Bar Chart" in ans:
            barChart(True)
        if "Histogram" in ans:
            Histogram()
        if "Parse" in ans:
            print(ParseData())
        print(ans)


chat()
