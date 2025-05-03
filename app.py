import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trainer Recommender", layout="centered")

# Load data
df = pd.read_csv("mock_trainer_dataset_realistic.csv")
df.columns = df.columns.str.strip()

# Get skills
skills_input = st.query_params.get("skills", [""])[0].strip()
user_skills = {s.strip().lower() for s in skills_input.split(",") if s.strip()}

st.title("🎯 Recommended Trainers")

if not user_skills:
    st.warning("Please enter at least one skill using ?skills=python,data analytics")
    st.stop()

# Debugging block
st.write("Your entered skills:", user_skills)

def score(skills_str):
    trainer_skills = {s.strip().lower() for s in str(skills_str).split(",")}
    return len(trainer_skills & user_skills)

df["Score"] = df["Skills"].apply(score)
df["Overlap"] = df["Skills"].apply(lambda x: {s.strip().lower() for s in str(x).split(",")} & user_skills)

# Show debug data
st.dataframe(df[["Trainer Name", "Skills", "Score", "Overlap"]])

# Filter and show
matches = df[df["Score"] > 0].sort_values("Score", ascending=False)

if matches.empty:
    st.error("❌ No matching trainers found.")
else:
    for _, row in matches.iterrows():
        st.subheader(row["Trainer Name"])
        st.markdown(f"**Skills:** {row['Skills']}")
        st.markdown(f"**Location:** {row['Location']}")
        st.markdown(f"**Experience:** {row['Years of Experience']} years")
        st.markdown(f"**Industry:** {row['Industry']}")
        st.markdown("---")
