import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv('mock_trainer_dataset_realistic.csv')

# Get query params
query = st.query_params
skills_input = query.get("skills", "")

st.title("🎯 Recommended Trainers for You")

if not skills_input:
    st.warning("Please submit the form first or use '?skills=python,excel' in the URL.")
else:
    input_skills = [s.strip().lower() for s in skills_input.split(',')]
    
    # Match score logic
    df['Match Score'] = df['Skills'].apply(
        lambda skills: len(set(skill.strip().lower() for skill in skills.split(',')) & set(input_skills))
    )

    results = df[df['Match Score'] > 0].sort_values(by='Match Score', ascending=False).head(5)

    if results.empty:
        st.info("No matching trainers found for the selected skills.")
    else:
        for _, row in results.iterrows():
            st.markdown(f"""
            ### 👨‍🏫 {row['Trainer Name']}
            - **Skills:** {row['Skills']}
            - **Location:** {row['Location']}
            - **Experience:** {row['Years of Experience']} years
            - **Certifications:** {row['Certifications']}
            - **Industry:** {row['Industry']}
            """)
