"""
This module provides a Dataset class that is used to clean, prepare and then return the dataset
for training purposes
"""

import logging
import numpy as np
import keras
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


class Preprocess(keras.layers.Layer):
    """
    Description: Prepares the dataset for training.
    Parameters: pandas dataframe, num of words (int)
    """

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

    def convert_texts_to_sequences(self, dataframe, text_only=False):
        """
            Description: Converts the data from texts to sequences of integer
            Params: dataframe(pandas dataframe), tokenizer
            Returns: sequences
        """
        
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        
        if text_only:
            sequences = tokenizer.texts_to_sequences(list(dataframe))
        else:
            # the fitted tokenizer now converts the text to integer sequences
            sequences = tokenizer.texts_to_sequences(list(dataframe["news"]))

        logging.info("The dataset is retrieved from the database and is preprocessed")

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

    def call(self):
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