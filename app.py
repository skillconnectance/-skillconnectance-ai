# app.py
import streamlit as st
import pandas as pd
from urllib.parse import parse_qs

# Page config
st.set_page_config(page_title="SkillConnectance - AI Engine", page_icon=":rocket:")

# Function to get skills from URL
def get_skills_from_url():
    query_params = st.experimental_get_query_params()
    skills_param = query_params.get('skills', [])
    if skills_param:
        return skills_param[0]  # Return the first (and usually only) skills string
    return ""

# Load Trainer Dataset
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('mock_trainer_dataset_realistic.csv')
        return data
    except Exception as e:
        st.error(f"Error loading trainer dataset: {e}")
        return None

trainers_df = load_data()

# Show Page
st.title("SkillConnectance - AI Engine 🚀")
st.write("Welcome to SkillConnectance AI Recommender System!")

# Auto-populate skills if coming from URL
url_skills = get_skills_from_url()

# User Input Section
st.subheader("Find Your Trainer:")

user_skills = st.text_input(
    "Enter skills you want to learn (comma-separated)",
    value=url_skills,
    placeholder="e.g., Python, Machine Learning, Data Analysis"
)

# Button to trigger matching
if st.button("Find Matching Trainers") or url_skills:
    if user_skills:
        user_skills_list = [skill.strip().lower() for skill in user_skills.split(",")]

        # Find Matching Trainers
        matching_trainers = []

        for index, row in trainers_df.iterrows():
            trainer_skills = [skill.strip().lower() for skill in row['Skills'].split(",")]
            matches = set(user_skills_list) & set(trainer_skills)
            if matches:
                matching_trainers.append((row['Trainer Name'], len(matches), ", ".join(matches), row['Location']))

        if matching_trainers:
            matching_trainers.sort(key=lambda x: x[1], reverse=True)

            st.subheader("Top Matching Trainers:")
            for trainer in matching_trainers[:5]:
                trainer_data = trainers_df[trainers_df['Trainer Name'] == trainer[0]].iloc[0]
                
                st.markdown(f"""
                **👤 Name:** {trainer_data['Trainer Name']}  
                **📍 Location:** {trainer_data['Location']}  
                **🧠 Matching Skills:** {trainer[2]}  
                **📅 Experience:** {trainer_data['Years of Experience']} years  
                **🎓 Certifications:** {trainer_data['Certifications']}  
                **🏢 Industry:** {trainer_data['Industry']}
                """)
                st.markdown("---")
        else:
            st.warning("No matching trainers found. Please try different skills.")
    else:
        st.warning("Please enter some skills to search!")
