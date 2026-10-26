
import streamlit as st
import requests

# Address of the Flask API. "backend" is the name of the backend container,
# Docker resolves it automatically because both containers are on the same network
BACKEND_URL = "http://backend:7860"

st.set_page_config(page_title="ExtraaLearn Lead Predictor")
st.title("ExtraaLearn - Lead Conversion Predictor")
st.write("Enter the details of a lead and click **Predict** to see how likely the lead is to become a paid customer.")

# Input fields
st.subheader("Lead details")
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=70, value=45)
    current_occupation = st.selectbox("Current occupation", ["Professional", "Unemployed", "Student"])
    first_interaction = st.selectbox("First interaction", ["Website", "Mobile App"])
    profile_completed = st.selectbox("Profile completed", ["High", "Medium", "Low"])
    last_activity = st.selectbox("Last activity", ["Email Activity", "Phone Activity", "Website Activity"])

with col2:
    website_visits = st.number_input("Website visits", min_value=0, max_value=50, value=3)
    time_spent_on_website = st.number_input("Time spent on website (seconds)", min_value=0, max_value=5000, value=400)
    page_views_per_visit = st.number_input("Page views per visit", min_value=0.0, max_value=20.0, value=3.0, step=0.1)

st.subheader("How did the lead hear about ExtraaLearn?")
col3, col4 = st.columns(2)

with col3:
    print_media_type1 = st.selectbox("Saw the ad in a newspaper", ["No", "Yes"])
    print_media_type2 = st.selectbox("Saw the ad in a magazine", ["No", "Yes"])
    digital_media = st.selectbox("Saw the ad on digital platforms", ["No", "Yes"])

with col4:
    educational_channels = st.selectbox("Heard on educational channels", ["No", "Yes"])
    referral = st.selectbox("Came through a referral", ["No", "Yes"])

# Data that is sent to the API (the keys are the same as the training columns)
lead = {
    "age": age,
    "current_occupation": current_occupation,
    "first_interaction": first_interaction,
    "profile_completed": profile_completed,
    "website_visits": website_visits,
    "time_spent_on_website": time_spent_on_website,
    "page_views_per_visit": page_views_per_visit,
    "last_activity": last_activity,
    "print_media_type1": print_media_type1,
    "print_media_type2": print_media_type2,
    "digital_media": digital_media,
    "educational_channels": educational_channels,
    "referral": referral,
}

if st.button("Predict", type="primary"):
    try:
        response = requests.post(BACKEND_URL + "/v1/predict", json=lead, timeout=60)
        if response.status_code == 200:
            result = response.json()
            probability = result["conversion_probability"] * 100
            st.metric("Probability of conversion", f"{probability:.1f}%")
            if result["prediction"] == 1:
                st.success("This lead is LIKELY to convert. Worth following up first.")
            else:
                st.warning("This lead is UNLIKELY to convert.")
        else:
            st.error("The API returned an error: " + response.text)
    except requests.exceptions.RequestException:
        st.error("Could not reach the API. Please check that the backend container is running.")
