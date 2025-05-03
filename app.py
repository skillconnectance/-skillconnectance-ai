import streamlit as st
import pandas as pd
from urllib.parse import unquote_plus

# Page config
st.set_page_config(page_title="Trainer Recommendations", layout="centered")

# Load trainer data
df = pd.read_csv("mock_trainer_dataset_realistic.csv")
df.columns = df.columns.str.strip()

st.title("🎯 SkillConnectance – Trainer Recommendations")

# Read & decode skills from URL (?skills=python,excel)
raw_skills = st.query_params.get("skills", [""])[0]
decoded_skills = unquote_plus(raw_skills)
user_skills = [s.strip().lower() for s in decoded_skills.split(",") if s.strip()]

if not user_skills:
    st.warning("No skills found. Please submit the form or add `?skills=python,excel` to the URL.")
    st.stop()

st.success(f"✅ Your entered skills: {', '.join(user_skills)}")

# Prepare trainer skills for matching
df["Skill List"] = (
    df["Skills"]
    .fillna("")
    .astype(str)
    .str.lower()
    .apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])
)

# Filter trainers by any matching skill
df["Matches"] = df["Skill List"].apply(lambda skills: bool(set(user_skills) & set(skills)))
matches = df[df["Matches"]]

if matches.empty:
    st.error("❌ No matching trainers found.")
else:
    st.subheader(f"🎓 Found {len(matches)} trainer(s):")
    for _, row in matches.iterrows():
        slug = row["Trainer Name"].strip().lower().replace(" ", "-").replace(".", "")
        profile_url = f"https://yourdomain.com/members/{slug}/"
        st.markdown(f"""
        **👤 {row['Trainer Name']}**  
        📍 {row['Location']}  
        🛠️ Skills: {', '.join(row['Skill List'])}  
        🏢 Industry: {row['Industry']}  
        ⏳ Experience: {row['Years of Experience']} years  
        🎓 Certifications: {row['Certifications']}  
        [🔗 View Full Profile]({profile_url})  
        """, unsafe_allow_html=True)
