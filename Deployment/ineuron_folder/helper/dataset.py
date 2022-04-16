"""
This module provides a Dataset class that is used to clean, prepare and then return the dataset
for training purposes
"""

import logging
import numpy as np
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.utils.np_utils import to_categorical
from sklearn import preprocessing
from preprocess import (
    lower_case,
    remove_special_characters,
    remove_stopwords,
    concatenate,
    lemmatize,
)


class Dataset:
    """
    Description: Prepares the dataset for training.
    Parameters: pandas dataframe, num of words (int)
    """

    def __init__(self, dataframe, num_words=2000):
        self.num_words = num_words
        self.dataframe = dataframe
        self.tokenizer = Tokenizer(num_words)
        self.dimension = 2000
        self.text = ""

    def preprocess(self, text):
        """
        Description: Preprocess Text Data
        Params: Text (str)
        Returns: Cleaned Text (Str)

        """

        self.text = text
        self.text = lower_case(self.text)
        self.text = remove_special_characters(self.text)
        self.text = remove_stopwords(self.text)
        self.text = concatenate(self.text)
        self.text = lemmatize(self.text)
        return self.text

    def get_tokenizer(self):
        """
            Description: Trains tokenizer on train set and returns it
            Params: None
            Returns: tokenizer
        """

        # builds the word index
        self.tokenizer.fit_on_texts(list(self.dataframe["news"]))

        return self.tokenizer

    def convert_texts_to_sequences(self, dataframe):
        """
            Description: Converts the data from texts to sequences of integer
            Params: dataframe(pandas dataframe), tokenizer
            Returns: sequences
        """

        # the fitted tokenizer now converts the text to integer sequences
        sequences = self.tokenizer.texts_to_sequences(list(dataframe["news"]))

        logging.info(
            "The dataset is retrieved from the database and is preprocessed")

        return sequences

    def vectorize_sequences(self, sequences, dimension=2000):
        """
            Description: Vectorizes sequences according to the dimensions.
                Step takes place after text to sequences.
            Params: sequences (vector of vector), dimension (int)
            Returns: result
        """

        self.dimension = dimension
        results = np.zeros((len(sequences), self.dimension))

        for i, sequence in enumerate(sequences):
            results[i, sequence] = 1.0

        return results

    def get_train_data(self):
        """
            Description: Returns training data in form of dense vectors
            Params: None
            Returns: train dataset
        """
        # applies preprocess function on the text data
        self.dataframe["news"] = self.dataframe["news"].apply(self.preprocess)

        # trains tokenizer on the cleaned data
        self.tokenizer = self.get_tokenizer()

        # converts the texts to sequences
        sequences = self.convert_texts_to_sequences(self.dataframe)

        # creates training dataset by converting sparse vectors to dense vectors
        train_dataset = self.vectorize_sequences(sequences)

        return train_dataset

    @staticmethod
    def get_labels(dataframe, target="category", get_encoder_only=False):
        """
            Description: Prepares labels of the dataframe
            Params: dataframe(pandas dataframe), tokenizer
            Returns: sequences
        """

        label_encoder = preprocessing.LabelEncoder()

        # Encode labels in column 'species'.
        dataframe[target] = label_encoder.fit_transform(dataframe[target])

        # get train labels from dataframe
        train_labels = dataframe[target]

        # converts the label to one hot encoding
        y_train = to_categorical(train_labels)

        if get_encoder_only:
            return label_encoder

        return y_train
