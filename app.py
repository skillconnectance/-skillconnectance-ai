import streamlit as st
import pandas as pd

# Load trainer data
df = pd.read_csv("mock_trainer_dataset_realistic.csv")

# Page config
st.set_page_config(page_title="Trainer Recommender", layout="wide")
st.title("🎯 SkillConnectance: Trainer Recommendations")

# Get skills from query params
query_params = st.query_params
raw_skills_input = query_params.get("skills", "")

st.markdown(f"🔍 **Debug query_params:**\n\n```json\n{query_params}\n```")
st.markdown(f"🪵 **Raw skills input from URL:** `{raw_skills_input}`")

if not raw_skills_input:
    st.warning("No skills found. Please submit the form or add '?skills=python,excel' to the URL.")
    st.stop()

# Normalize user-entered skills
user_skills = [s.strip().lower() for s in raw_skills_input.split(",") if s.strip()]
st.success(f"✅ Your entered skills: `{', '.join(user_skills)}`")

# Ensure trainer 'Skills' column is lowercase string
df["Skills"] = df["Skills"].fillna("").astype(str).str.lower()

# Score trainers based on skill overlap
def score_trainer(skills_text):
    trainer_skills = [s.strip() for s in skills_text.split(",")]
    return len(set(user_skills) & set(trainer_skills))

df["Score"] = df["Skills"].apply(score_trainer)
df_filtered = df[df["Score"] > 0].sort_values(by="Score", ascending=False)

if df_filtered.empty:
    st.error("❌ No matching trainers found.")
else:
    st.subheader("🎓 Recommended Trainers for You:")
    for _, row in df_filtered.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            **👤 Name:** {row['Trainer Name']}  
            **📍 Location:** {row['Location']}  
            **💼 Industry:** {row['Industry']}  
            **🧠 Skills:** {row['Skills']}  
            **🎖️ Experience:** {row['Years of Experience']} years  
            **📜 Certifications:** {row['Certifications']}
            """)
        with col2:
            # BuddyBoss profile URL logic
            if 'BuddyBoss URL' in row and pd.notna(row['BuddyBoss URL']):
                st.link_button("🔗 View Profile", row['BuddyBoss URL'])
            else:
                st.button("Profile Coming Soon", disabled=True)
