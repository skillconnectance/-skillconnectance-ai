import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("mock_trainer_dataset_realistic.csv")

df = load_data()
st.set_page_config(page_title="Trainer Recommender", layout="centered")

st.title("🎯 Skill-Based Trainer Recommender")
skill_input = st.text_input("Enter a skill:")

if skill_input:
    filtered_df = df[df['Skills'].str.contains(skill_input, case=False, na=False)]
    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            with st.expander(f"{row['Trainer Name']} — {row['Skills']}"):
                st.write(f"**Location:** {row['Location']}")
                st.write(f"**Experience:** {row['Years of Experience']} years")
                st.write(f"**Certifications:** {row['Certifications']}")
                st.write(f"**Industry:** {row['Industry']}")
                
                profile_url = row.get('ProfileURL', '#')
                st.markdown(f"[🔗 View Full Profile ↗]({profile_url})", unsafe_allow_html=True)
    else:
        st.warning("No matching trainers found.")
else:
    st.info("Start by entering a skill above.")
