"""
This module provides functions for preprocessing text data.
"""

import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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
