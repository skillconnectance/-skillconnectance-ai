import streamlit as st
import pandas as pd

# Load your dataset
@st.cache_data
def load_data():
    return pd.read_csv("mock_trainer_dataset_realistic.csv")  # Make sure this file is in your repo

df = load_data()

# Page setup
st.set_page_config(page_title="Trainer Recommendation", layout="centered")

# Title and input
st.title("🔍 Find the Right Trainer for Your Skill")

skill_input = st.text_input("Enter your desired skill (e.g., Python, Excel):")

# Filter and display results
if skill_input:
    filtered_df = df[df['Skills'].str.contains(skill_input, case=False, na=False)]
    
    if not filtered_df.empty:
        st.success(f"Found {len(filtered_df)} matching trainer(s)!")
        st.dataframe(filtered_df[['Name', 'Skills', 'Location', 'Rating']])
    else:
        st.warning("No matching trainers found. Try a broader or different skill.")
