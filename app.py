import streamlit as st
import pandas as pd
import urllib

# Load dataset
df = pd.read_csv("mock_trainer_dataset_realistic.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Get skills from URL
query_params = st.experimental_get_query_params()
user_skills = query_params.get("skills", [""])[0].lower().split(",")

st.title("🎯 Recommended Trainers")

# Filter trainers
def match_skills(row):
    trainer_skills = str(row['Skills']).lower().split(",")
    return any(skill.strip() in trainer_skills for skill in user_skills)

filtered_df = df[df.apply(match_skills, axis=1)]

if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
        <div style="border:1px solid #ccc; border-radius:10px; padding:15px; margin-bottom:10px;">
            <h4>{row['Trainer Name']}</h4>
            <b>Skills:</b> {row['Skills']}<br>
            <b>Location:</b> {row['Location']}<br>
            <b>Experience:</b> {row['Years of Experience']} years<br>
            <b>Certifications:</b> {row['Certifications']}<br>
            <b>Industry:</b> {row['Industry']}<br><br>
            <a href="{row['BuddyBoss Profile URL']}" target="_blank">
                <button>View Full Trainer Profile</button>
            </a>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No matching trainers found for those skills.")
