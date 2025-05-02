import streamlit as st
import pandas as pd

# Load trainer data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("mock_trainer_dataset_realistic.csv")
        return df
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return pd.DataFrame()

df = load_data()

st.set_page_config(page_title="Trainer Recommender", layout="centered")
st.title("🎯 Skill-Based Trainer Recommender")

st.markdown("Enter a skill and use filters to discover the most relevant trainers for you.")

# Skill input
skill_input = st.text_input("Enter a skill (e.g., Python, Excel, Communication):")

# Optional filters
col1, col2 = st.columns(2)
with col1:
    selected_location = st.selectbox("📍 Filter by Location", options=["All"] + sorted(df['Location'].dropna().unique().tolist()))
with col2:
    selected_industry = st.selectbox("🏭 Filter by Industry", options=["All"] + sorted(df['Industry'].dropna().unique().tolist()))

# Apply filters
if skill_input:
    filtered_df = df[df['Skills'].str.contains(skill_input, case=False, na=False)]

    if selected_location != "All":
        filtered_df = filtered_df[filtered_df['Location'] == selected_location]

    if selected_industry != "All":
        filtered_df = filtered_df[filtered_df['Industry'] == selected_industry]

    if not filtered_df.empty:
        st.success(f"✅ Found {len(filtered_df)} trainer(s).")

        for _, row in filtered_df.iterrows():
            with st.expander(f"👤 {row['Trainer Name']} — {row['Skills']}"):
                st.write(f"**📍 Location:** {row['Location']}")
                st.write(f"**🕐 Experience:** {row['Years of Experience']} years")
                st.write(f"**🎓 Certifications:** {row['Certifications']}")
                st.write(f"**🏭 Industry:** {row['Industry']}")
                
                # Replace below URL with real BuddyBoss profile URL if available
                profile_url = f"https://yourdomain.com/trainer-profile/{row['Trainer Name'].replace(' ', '-').lower()}"
                st.markdown(f"[🔗 View Full Profile]({profile_url})", unsafe_allow_html=True)
    else:
        st.warning("❌ No trainers match your filters. Try different keywords or remove filters.")
else:
    st.info("🔍 Start by entering a skill above.")
