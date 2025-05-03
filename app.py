import streamlit as st
import pandas as pd

# Debug: comment this out once params work
# st.write("👀 Query Params:", st.query_params)

df = pd.read_csv('mock_trainer_dataset_realistic.csv')
df.columns = df.columns.str.strip()

# Read the skills param
skills_input = st.query_params.get("skills", [""])[0]

st.set_page_config(page_title="Trainer Recommendations", layout="centered")
st.title("🎯 Recommended Trainers for You")

if not skills_input:
    st.warning("No skills found. Please retry the form or add '?skills=python,excel' to the URL.")
else:
    input_skills = [s.strip().lower() for s in skills_input.split(",")]

    df['Match Score'] = df['Skills'].apply(
        lambda skill_str: len(
            set(s.strip().lower() for s in skill_str.split(",")) & set(input_skills)
        )
    )
    results = df[df['Match Score'] > 0].sort_values("Match Score", ascending=False)

    if results.empty:
        st.info("No matching trainers found for those skills.")
    else:
        for _, row in results.iterrows():
            slug = row['Trainer Name'].strip().lower().replace(" ", "-").replace(".", "")
            url = f"https://yourdomain.com/members/{slug}/"
            card = f"""
            <div style="border:1px solid #ccc; padding:15px; border-radius:10px; margin-bottom:10px;">
              <h4>{row['Trainer Name']}</h4>
              <p><b>Skills:</b> {row['Skills']}</p>
              <p><b>Location:</b> {row['Location']}</p>
              <p><b>Experience:</b> {row['Years of Experience']} years</p>
              <p><b>Certifications:</b> {row['Certifications']}</p>
              <p><b>Industry:</b> {row['Industry']}</p>
              <a href="{url}" target="_blank" style="display:inline-block; padding:8px 15px; background:#0073aa; color:#fff; text-decoration:none; border-radius:5px;">
                View Full Profile
              </a>
            </div>
            """
            st.markdown(card, unsafe_allow_html=True)
