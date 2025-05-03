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

    # Match trainers based on skills
    df['Match Score'] = df['Skills'].apply(
        lambda skills: len(set(skill.strip().lower() for skill in skills.split(',')) & set(input_skills))
    )

    results = df[df['Match Score'] > 0].sort_values(by='Match Score', ascending=False).head(5)

    if results.empty:
        st.info("No matching trainers found for the selected skills.")
    else:
        for _, row in results.iterrows():
            # Construct profile URL (temporary placeholder for now)
            trainer_slug = row['Trainer Name'].lower().replace(" ", "-")
            profile_url = f"https://yourdomain.com/members/{trainer_slug}/"

            # Display trainer details
            st.markdown(f"""
            ### 👨‍🏫 {row['Trainer Name']}
            - **Skills:** {row['Skills']}
            - **Location:** {row['Location']}
            - **Experience:** {row['Years of Experience']} years
            - **Certifications:** {row['Certifications']}
            - **Industry:** {row['Industry']}
            """)
            
            # Add "View Profile" button
            st.markdown(f'<a href="{profile_url}" target="_blank"><button>View Profile</button></a>', unsafe_allow_html=True)
