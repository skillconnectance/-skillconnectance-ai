import streamlit as st
import pandas as pd
from urllib.parse import unquote_plus

st.set_page_config(page_title="Trainer Recommender", layout="centered")

# Load dataset
df = pd.read_csv("mock_trainer_dataset_realistic.csv")
df.columns = df.columns.str.strip()  # Clean column names

# 🧠 Get & decode skills from URL
raw_skills = st.query_params.get("skills", [""])[0]
decoded_skills = unquote_plus(raw_skills)  # Converts + and %2C properly
user_skills = {s.strip().lower() for s in decoded_skills.split(",") if s.strip()}

st.title("🎯 Recommended Trainers")

if not user_skills:
    st.warning("No skills detected. Please use a URL like `?skills=python,data analytics`")
    st.stop()

st.write("✅ Your entered skills:", user_skills)

# 🧠 Matching logic
def score(trainer_skill_str):
    trainer_skills = {s.strip().lower() for s in str(trainer_skill_str).split(",")}
    return len(trainer_skills & user_skills)

df["Score"] = df["Skills"].apply(score)
df["Matched Skills"] = df["Skills"].apply(lambda s: {x.strip().lower() for x in str(s).split(",")} & user_skills)

matches = df[df["Score"] > 0].sort_values(by="Score", ascending=False)

if matches.empty:
    st.error("❌ No matching trainers found.")
else:
    for _, row in matches.iterrows():
        st.subheader(row["Trainer Name"])
        st.markdown(f"**Skills:** {row['Skills']}")
        st.markdown(f"**Location:** {row['Location']}")
        st.markdown(f"**Experience:** {row['Years of Experience']} years")
        st.markdown(f"**Industry:** {row['Industry']}")
        # Optional: Add a dummy profile button until BuddyBoss URLs are added
        st.markdown(f"[🔗 View Profile](https://skillconnectance.com/trainers/{row['Trainer Name'].replace(' ', '-').lower()})", unsafe_allow_html=True)
        st.markdown("---")
