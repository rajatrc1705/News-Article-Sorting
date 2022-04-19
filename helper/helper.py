"""
This python file contains all the helper functions required by the model to process the input and give an output.
"""

import os
import pickle
import numpy as np
import pandas as pd
from tensorflow import keras
import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import streamlit as st

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")


def remove_stopwords(text):
    """
    Description: Removes stopwords like 'is', 'an', 'the' from the input string.
    Params:
        text: str
    Returns:
        text: str
    """

    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    return " ".join([x for x in words if x not in stop_words])


def lemmatize(text):
    """
    Description: Lemmatizes input string. eg: Bats -> Bat
    Params:
        text: str
    Returns:
        text: str
    """

    text = text.split()
    wordnet = WordNetLemmatizer()
    return " ".join([wordnet.lemmatize(word) for word in text])


def concatenate(text):
    """
    Description: Ensures evenly spaced words in the input string.
        eg: 'Hello Harry! So   nice to     see you  '
            to
            'Hello Harry! So nice to see you'
    Params:
        text: str
    Returns:
        text: str
    """

    text = text.split()
    return " ".join(text)


def lower_case(text):
    """
    Description: Makes all characters lower case.
    Params:
        text: str
    Returns:
        text: str
    """

    return text.lower()


def remove_special_characters(text):
    """
    Description: Removes <br> tags and any other characters except alphabets and apostrophe.
    Params:
        text: str
    Returns:
        text: str
    """

    text = re.sub("<br\\s*/?>", " ", text)
    text = re.sub("[^a-zA-Z']", " ", text)
    text = re.sub("-", " ", text)
    return text

# loading the tokenizer


print(os.getcwd())
with open('static/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# loading the label_encoder
with open('static/label_encoder.pickle', 'rb') as handle:
    label_encoder = pickle.load(handle)

# loading the model
model = keras.models.load_model('static/news_classification_model_4.h5')


def preprocess_text(inputs, dimension=2000):
    """
    Parameters: 
        inputs (str): The text string to be preprocessed
        dimension (int): The number of words considered by the tokenizer
    Returns:
        results:
            Sequence 
    """
    inputs = lower_case(inputs)
    inputs = remove_special_characters(inputs)
    inputs = remove_stopwords(inputs)
    inputs = concatenate(inputs)
    inputs = lemmatize(inputs)

    inputs = [inputs]

    sequences = tokenizer.texts_to_sequences(inputs)

    results = np.zeros((len(sequences), dimension))

    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.0

    return results


def result(category):
    """
    Parameters:
        category (list of numbers): The probability of each class, which the model thinks the news article belongs to.
    Returns:
        The actual category in string format
    """
    return label_encoder.inverse_transform([category[0].argmax()])[0]


def predictor(input_text):
    """
    Parameters:
        input_text (str): The raw, uncleaned text input to be received from the user
    Returns:
        output (str): The class predicted by model, to which the news input belongs
    """

    cleaned_input_text = preprocess_text(input_text)
    category = model.predict(cleaned_input_text)
    prediction_probability = category[0]
    x_axis = [label_encoder.inverse_transform(
        [i])[0] for i in np.array(range(5))]
    df = pd.DataFrame(
        {'Categories': x_axis, 'Confidence': prediction_probability})
    df = df.set_index('Categories')
    st.bar_chart(df)
    output = result(category)

    return output
