import streamlit as st
import pandas as pd

# Load the trainer dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("mock_trainer_dataset_realistic.csv")  # Updated filename here
        return df
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return pd.DataFrame()

df = load_data()

st.set_page_config(page_title="Trainer Recommender", layout="centered")
st.title("🎯 Skill-Based Trainer Recommender")
st.markdown("Enter a skill to find trainers who offer training in that domain.")

# Debug: show available columns
st.write("📋 Dataset columns:", df.columns.tolist())

# Input box
skill_input = st.text_input("Enter a skill (e.g., Python, Excel, Communication):")

# Filter and show results
if skill_input:
    filtered_df = df[df['Skills'].str.contains(skill_input, case=False, na=False)]

    if not filtered_df.empty:
        st.success(f"✅ Found {len(filtered_df)} trainer(s) with that skill.")

        # Display safe subset of columns
        display_columns = ['Trainer Name', 'Skills', 'Location', 'Years of Experience', 'Certifications', 'Industry']
        available_columns = [col for col in display_columns if col in filtered_df.columns]
        st.dataframe(filtered_df[available_columns])
    else:
        st.warning("❌ No matching trainers found. Try a broader or alternative skill.")
