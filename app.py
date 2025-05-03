import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv('mock_trainer_dataset_realistic.csv')

# Clean column names (remove extra spaces if any)
df.columns = df.columns.str.strip()

# Retrieve 'Desired Skills to Learn' from the URL query params
query = st.query_params
skills_input = query.get("Desired Skills to Learn", "")

st.title("🎯 Recommended Trainers for You")

if not skills_input:
    st.warning("No skills found. Please submit the form or add '?Desired Skills to Learn=python,data analytics' to the URL.")
else:
    # Process input skills
    input_skills = [s.strip().lower() for s in skills_input.split(',')]

    # Calculate match score
    df['Match Score'] = df['Skills'].apply(
        lambda skills: len(set(skill.strip().lower() for skill in skills.split(',')) & set(input_skills))
    )

    # Filter top matches
    results = df[df['Match Score'] > 0].sort_values(by='Match Score', ascending=False)

    if results.empty:
        st.info("No matching trainers found for those skills.")
    else:
        for _, row in results.iterrows():
            trainer_name = row['Trainer Name']
            
            # Generate slug from trainer name for profile URL 
            slug = trainer_name.strip().lower().replace(' ', '-').replace('.', '')
            profile_url = f"https://yourdomain.com/members/{slug}/"

            # Display trainer details
            st.markdown(f"""
            <div style="border: 1px solid #ccc; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <h4>{trainer_name}</h4>
                <b>Skills:</b> {row['Skills']}<br>
                <b>Location:</b> {row['Location']}<br>
                <b>Experience
