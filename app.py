# app.py
import streamlit as st
import pandas as pd

# Set Streamlit page config
st.set_page_config(page_title="SkillConnectance - AI Engine", page_icon=":rocket:")

# Title
st.title("SkillConnectance - AI Engine 🚀")
st.write("Welcome to SkillConnectance AI Recommender System!")

# Load Trainer Dataset
@st.cache_data
def load_data():
    data = pd.read_csv('mock_trainer_dataset_realistic.csv')
    return data

trainers_df = load_data()

# Display Dataset Preview
st.subheader("Available Trainers:")
st.dataframe(trainers_df)
