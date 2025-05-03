import streamlit as st
import pandas as pd
from urllib.parse import unquote_plus

# — Page config
st.set_page_config(page_title="Trainer Recommendations", layout="centered")
st.title("🎯 SkillConnectance – Trainer Recommendations")

# — Load your trainer dataset
df = pd.read_csv("mock_trainer_dataset_realistic.csv")
df.columns = df.columns.str.strip()  # trim stray spaces

# — Parse the 'skills' query param robustly
param = st.query_params.get("skills")

if isinstance(param, list) and param:
    raw = param[0]
elif isinstance(param, str):
    raw = param
else:
    raw = ""

# Decode URL-encoded characters (spaces as + or %20)
decoded = unquote_plus(raw)

# Build the user_skills list
user_skills = [s.strip().lower() for s in decoded.split(",") if s.strip()]

# — If no skills, prompt and stop
if not user_skills:
    st.warning(
        "No skills detected. Please submit the form so you land here with "
        "`?skills=python,data analytics` in the URL."
    )
    st.stop()

st.success(f"✅ Your entered skills: {', '.join(user_skills)}")

# — Prepare trainer skills for matching
df["Skill List"] = (
    df["Skills"]
      .fillna("")
      .astype(str)
      .str.lower()
      .apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])
)

# — Filter trainers: any overlap
def has_overlap(tr_skills, usr_skills):
    return bool(set(tr_skills) & set(usr_skills))

df["Match"] = df["Skill List"].apply(lambda skills: has_overlap(skills, user_skills))
matches = df[df["Match"]]

# — Show results
if matches.empty:
    st.error("❌ No matching trainers found for those skills.")
else:
    st.subheader(f"🎓 Found {len(matches)} trainer(s):")
    for _, row in matches.iterrows():
        slug = row["Trainer Name"].strip().lower().replace(" ", "-").replace(".", "")
        profile_url = f"https://yourdomain.com/members/{slug}/"

        st.markdown(f"""
        **👤 Name:** {row['Trainer Name']}  
        **📍 Location:** {row['Location']}  
        **🛠️ Skills:** {', '.join(row['Skill List'])}  
        **🏢 Industry:** {row['Industry']}  
        **⏳ Experience:** {row['Years of Experience']} years  
        **🎓 Certifications:** {row['Certifications']}  
        [🔗 View Full Profile]({profile_url})
        """, unsafe_allow_html=True)
