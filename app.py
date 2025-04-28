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
# User Input Section
st.subheader("Find Your Trainer:")

user_skills = st.text_input("Enter skills you want to learn (comma-separated)", placeholder="e.g., Python, Machine Learning, Data Analysis")

# Button to trigger matching
if st.button("Find Matching Trainers"):
    if user_skills:
        user_skills_list = [skill.strip().lower() for skill in user_skills.split(",")]

        # Find Matching Trainers
        matching_trainers = []

        for index, row in trainers_df.iterrows():
            trainer_skills = [skill.strip().lower() for skill in row['Skills'].split(",")]
            matches = set(user_skills_list) & set(trainer_skills)
            if matches:
                matching_trainers.append((row['Name'], len(matches), ", ".join(matches), row['Location']))

        if matching_trainers:
            # Sort trainers by number of matches (most relevant first)
            matching_trainers.sort(key=lambda x: x[1], reverse=True)

            # Display top matches
            st.subheader("Top Matching Trainers:")
            for trainer in matching_trainers[:5]:
                st.markdown(f"**Name:** {trainer[0]}  \n**Matching Skills:** {trainer[2]}  \n**Location:** {trainer[3]}")
                st.markdown("---")
        else:
            st.warning("No matching trainers found. Please try different skills.")
    else:
        st.warning("Please enter some skills to search!")
