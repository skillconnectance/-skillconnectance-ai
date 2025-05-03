import streamlit as st
import requests
from urllib.parse import unquote_plus

# — Page config
st.set_page_config(page_title="Trainer Recommendations", layout="centered")
st.title("🎯 SkillConnectance – Trainer Recommendations")

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

# — Prepare API URL with query parameters for the backend
api_url = f"http://127.0.0.1:8000/recommend_trainer?skills={','.join(user_skills)}"

# Call the API to get trainer recommendations
try:
    response = requests.get(api_url)
    if response.status_code == 200:
        trainers = response.json()['recommended_trainers']
        
        if not trainers:
            st.error("❌ No matching trainers found for those skills.")
        else:
            st.subheader(f"🎓 Found {len(trainers)} trainer(s):")
            for trainer in trainers:
                trainer_name = trainer['name']
                matched_skills = ', '.join(trainer['matched_skills'])

                # Example URL, assuming a generic profile structure
                slug = trainer_name.strip().lower().replace(" ", "-").replace(".", "")
                profile_url = f"https://yourdomain.com/members/{slug}/"

                # Display trainer info
                st.markdown(f"""
                **👤 Name:** {trainer_name}  
                **🛠️ Matched Skills:** {matched_skills}  
                [🔗 View Full Profile]({profile_url})
                """, unsafe_allow_html=True)
    else:
        st.error(f"Error: Unable to fetch data from the API. Status code {response.status_code}")
except Exception as e:
    st.error(f"Error: {e}")
