import streamlit as st
import pandas as pd

# Load data from CSV
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("trainers.csv")
        return df
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return pd.DataFrame()

df = load_data()

# Streamlit Page Config
st.set_page_config(page_title="Trainer Recommender", layout="centered")

# UI
st.title("🎯 Find the Right Trainer for Your Skill")
st.markdown("Type in a skill to see matching trainers from our platform.")

# Debug helper (remove later if you want)
if df.empty:
    st.warning("⚠️ No data loaded. Please check if `trainers.csv` exists in your repo.")
    st.stop()
else:
    st.write("📋 Available columns:", df.columns.tolist())

# Input
skill_input = st.text_input("Enter a skill (e.g., Python, Excel, Marketing):")

# Filter + Result
if skill_input:
    filtered_df = df[df['Skills'].str.contains(skill_input, case=False, na=False)]
    
    if not filtered_df.empty:
        st.success(f"✅ Found {len(filtered_df)} trainer(s) matching your skill.")
        
        # Only display existing columns to prevent KeyErrors
        expected_columns = ['Name', 'Skills', 'Location', 'Rating']
        available_columns = [col for col in expected_columns if col in filtered_df.columns]
        
        st.dataframe(filtered_df[available_columns])
    else:
        st.warning("❌ No matching trainers found. Try a broader or alternate skill.")

