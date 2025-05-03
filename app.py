import pandas as pd
import streamlit as st

# Load the trainers CSV
trainers_df = pd.read_csv('mock_trainer_dataset_realistic.csv')

# Convert 'Skills' column to lowercase for case-insensitive matching
trainers_df['Skills'] = trainers_df['Skills'].str.lower()

# Streamlit user input for skills
query_params = st.experimental_get_query_params()

# Check if the 'skills' parameter is in the query params
if 'skills' in query_params:
    raw_skills_input = query_params['skills'][0]
    skills = [skill.strip().lower() for skill in raw_skills_input.split(',')]
    st.write(f"✅ Your entered skills: {', '.join(skills)}")

    # Filter the dataframe to find trainers matching any of the entered skills
    filtered_trainers = trainers_df[trainers_df['Skills'].apply(
        lambda x: any(skill in x for skill in skills))]

    if not filtered_trainers.empty:
        st.write("📝 Matching trainers found:")
        st.dataframe(filtered_trainers[['Trainer Name', 'Skills', 'Location', 'Years of Experience', 'Certifications', 'Industry']])
        for index, row in filtered_trainers.iterrows():
            # Assuming you have the BuddyBoss profile URL in the CSV (manually add in the future)
            st.markdown(f"[View Profile]({row['BuddyBoss Profile URL']})")
    else:
        st.write("❌ No matching trainers found.")
else:
    st.write("❌ Please submit the form or add '?skills=python,excel' to the URL.")
