from helper import helper as hp

import streamlit as st

import os

# title of the streamlit application
st.title("News Article Classification")

user_input = st.text_area("News Article That You Want To Classify", "eg: -  Football is the most widely played sport in the world.")

if st.button('Predict'):
    output = hp.predictor(user_input)
    st.success(f'Prediction: - {output.upper()}')
