# app.py
import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="SkillConnectance - AI Engine", page_icon=":rocket:")

# Title
st.title("SkillConnectance - AI Engine 🚀")
st.write("Welcome to SkillConnectance AI Recommender System!")

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

# Display Dataset Preview
if trainers_df is not None:
    st.subheader("Available Trainers:")
    st.dataframe(trainers_df)

# After matching_trainers is built

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
