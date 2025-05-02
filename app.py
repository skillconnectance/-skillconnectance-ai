import streamlit as st
import pandas as pd
import difflib
from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from streamlit.web import bootstrap

# Load trainer data
df = pd.read_csv("mock_trainer_dataset_realistic.csv")

# Normalize column names
df.columns = df.columns.str.strip()

# FastAPI instance
api = FastAPI()

def get_top_matches(user_skills: str, top_n: int = 5):
    user_skills_list = [skill.strip().lower() for skill in user_skills.split(",")]
    matching_trainers = []

    for _, row in df.iterrows():
        trainer_skills = [skill.strip().lower() for skill in str(row['Skills']).split(",")]
        matches = list(set(user_skills_list) & set(trainer_skills))
        if matches:
            matching_trainers.append({
                "name": row['Trainer Name'],
                "matching_skills": matches,
                "location": row['Location'],
                "match_score": len(matches)
            })

    # Sort by match score (descending)
    matching_trainers.sort(key=lambda x: x['match_score'], reverse=True)

    return matching_trainers[:top_n]

# Streamlit UI for manual testing
st.title("🔍 SkillConnect Trainer Recommender")

user_input = st.text_input("Enter skills (comma-separated):")
if st.button("Find Trainers"):
    if user_input:
        results = get_top_matches(user_input)
        if results:
            for trainer in results:
                st.markdown(f"**Name:** {trainer['name']}")
                st.markdown(f"**Matching Skills:** {', '.join(trainer['matching_skills'])}")
                st.markdown(f"**Location:** {trainer['location']}")
                st.markdown("---")
        else:
            st.warning("No matching trainers found.")
    else:
        st.warning("Please enter at least one skill.")

# API route for webhook integration
@api.post("/recommend")
async def recommend(request: Request):
    data = await request.json()
    user_skills = data.get("skills", "")
    if not user_skills:
        return JSONResponse(content={"error": "No skills provided"}, status_code=400)

    top_matches = get_top_matches(user_skills)
    return JSONResponse(content={"recommendations": top_matches})

# Run FastAPI inside Streamlit (for local dev, not needed on Streamlit Cloud)
def run():
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8501)

# Uncomment the line below to run API only (for local testing)
# run()
