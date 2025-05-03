import streamlit as st

st.write("👀 Query Params:", st.query_params)

import pandas as pd

# Load dataset
df = pd.read_csv('mock_trainer_dataset_realistic.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Retrieve 'Desired Skills to Learn' from the URL query params
query = st.query_params
skills_input = query.get("Desired Skills to Learn", [""])[0]

st.set_page_config(page_title="Trainer Recommendations", layout="centered")
st.title("🎯 Recommended Trainers for You")

if not skills_input:
    st.warning(
        "No skills found. Please submit the form or add "
        "'?Desired Skills to Learn=python,data analytics' to the URL."
    )
else:
    # Process input skills
    input_skills = [s.strip().lower() for s in skills_input.split(',')]

    # Calculate match score
    def calc_score(skills_str):
        skills_set = {s.strip().lower() for s in skills_str.split(',')}
        return len(skills_set & set(input_skills))

    df['Match Score'] = df['Skills'].apply(calc_score)

    # Filter and sort
    results = df[df['Match Score'] > 0].sort_values(by='Match Score', ascending=False)

    if results.empty:
        st.info("No matching trainers found for those skills.")
    else:
        for _, row in results.iterrows():
            trainer_name = row['Trainer Name']
            # Generate slug from trainer name
            slug = (
                trainer_name
                .strip()
                .lower()
                .replace(' ', '-')
                .replace('.', '')
            )
            profile_url = f"https://yourdomain.com/members/{slug}/"

            # Render trainer card
            card_html = f"""
            <div style="
                border: 1px solid #ccc;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 10px;
            ">
                <h4>{trainer_name}</h4>
                <p><b>Skills:</b> {row['Skills']}</p>
                <p><b>Location:</b> {row['Location']}</p>
                <p><b>Experience:</b> {row['Years of Experience']} years</p>
                <p><b>Certifications:</b> {row['Certifications']}</p>
                <p><b>Industry:</b> {row['Industry']}</p>
                <a href="{profile_url}" target="_blank" style="
                    display: inline-block;
                    padding: 8px 15px;
                    background-color: #0073aa;
                    color: #fff;
                    text-decoration: none;
                    border-radius: 5px;
                ">View Full Profile</a>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
