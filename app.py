import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trainer Recommendations", layout="centered")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("mock_trainer_dataset_realistic.csv")

df = load_data()

st.title("🎯 SkillConnectance – Trainer Recommendations")

# Get query param from URL: ?skills=python,data analytics
raw_skills = st.query_params.get("skills")
if raw_skills:
    skills_input = raw_skills[0]
    user_skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
else:
    user_skills = []

if not user_skills:
    st.warning("No skills found. Please submit the form or add `?skills=python,data analytics` to the URL.")
    st.stop()

st.success(f"✅ Your entered skills: {set(user_skills)}")

# Preprocess trainer data
df["Skills"] = df["Skills"].astype(str).str.lower()
df["Skill List"] = df["Skills"].apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])

# Match trainers
def matches(trainer_skills, user_skills):
    return any(skill in trainer_skills for skill in user_skills)

df["Match"] = df["Skill List"].apply(lambda skills: matches(skills, user_skills))
matching_trainers = df[df["Match"]]

if matching_trainers.empty:
    st.error("❌ No matching trainers found.")
else:
    st.subheader(f"✅ Found {len(matching_trainers)} matching trainer(s):")
    for _, row in matching_trainers.iterrows():
        st.markdown(f"""
        **👤 Trainer Name:** {row['Trainer Name']}  
        **📍 Location:** {row['Location']}  
        **📚 Skills:** {row['Skills']}  
        **🏢 Industry:** {row['Industry']}  
        **🧪 Experience:** {row['Years of Experience']} years  
        **🎓 Certifications:** {row['Certifications']}  
        """, unsafe_allow_html=True)

        # Add a profile button if URL exists (optional column)
        profile_url = row.get("BuddyBoss Profile URL", None)
        if pd.notna(profile_url) and isinstance(profile_url, str) and profile_url.startswith("http"):
            st.markdown(f"[👉 View Full Profile]({profile_url})", unsafe_allow_html=True)
        else:
            st.markdown("*Profile link not available.*")

        st.markdown("---")
