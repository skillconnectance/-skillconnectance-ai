import streamlit as st
import pandas as pd

# — Page config
st.set_page_config(page_title="Trainer Recommendations", layout="centered")

# — Load trainer data
df = pd.read_csv("mock_trainer_dataset_realistic.csv")
df.columns = df.columns.str.strip()  # strip any stray spaces

# — Get skills list from URL (?skills=python,excel)
skills_input = st.query_params.get("skills", [""])[0].strip()

st.title("🎯 Recommended Trainers for You")

if not skills_input:
    st.warning(
        "No skills detected. Please submit the form so you land here with "
        "`?skills=python,excel` in the URL."
    )
else:
    # normalize user skills
    user_skills = {s.strip().lower() for s in skills_input.split(",") if s.strip()}

    # compute match score (# of overlapping skills)
    def calc_score(sk_str):
        trainer_skills = {t.strip().lower() for t in str(sk_str).split(",")}
        return len(trainer_skills & user_skills)

    df["Match Score"] = df["Skills"].apply(calc_score)

    # filter and sort
    results = df[df["Match Score"] > 0].sort_values("Match Score", ascending=False)

    if results.empty:
        st.info("No matching trainers found for those skills.")
    else:
        for _, row in results.iterrows():
            name = row["Trainer Name"]
            # build BuddyBoss profile URL slug
            slug = name.strip().lower().replace(" ", "-").replace(".", "")
            profile_url = f"https://yourdomain.com/members/{slug}/"

            # render trainer card
            card = f"""
            <div style="
              border:1px solid #ccc;
              padding:15px;
              border-radius:10px;
              margin-bottom:15px;
            ">
              <h4 style="margin:0 0 8px 0;">👨‍🏫 {name}</h4>
              <p style="margin:4px 0;"><strong>Skills:</strong> {row["Skills"]}</p>
              <p style="margin:4px 0;"><strong>Location:</strong> {row["Location"]}</p>
              <p style="margin:4px 0;"><strong>Experience:</strong> {row["Years of Experience"]} years</p>
              <p style="margin:4px 0;"><strong>Certifications:</strong> {row["Certifications"]}</p>
              <p style="margin:4px 0 12px 0;"><strong>Industry:</strong> {row["Industry"]}</p>
              <a href="{profile_url}" target="_blank" style="
                  display:inline-block;
                  padding:8px 16px;
                  background-color:#0073aa;
                  color:#ffffff;
                  text-decoration:none;
                  border-radius:5px;
              ">View Full Profile</a>
            </div>
            """
            st.markdown(card, unsafe_allow_html=True)
