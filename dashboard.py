import streamlit as st
import requests

st.set_page_config(page_title="Tailing Dam Monitor", page_icon="🏗️")

st.title("🏗️ Tailing Dam Data Portal")
st.write("Secure API Access for Geophysical Calculations")

# 1. Setup the Connection Info
# Replace this with your actual Render URL!
API_URL = "https://api-keys-izl8.onrender.com/multiply"

# 2. Sidebar for Authentication
st.sidebar.header("Authentication")
user_key = st.sidebar.text_input("Enter your API Key", type="password")

# 3. Main Interface
st.subheader("Calculation Tool")
number_input = st.number_input("Enter a value to process (e.g., Sensor Reading):", value=1.0)

if st.button("Calculate"):
    if not user_key:
        st.error("Please enter an API Key in the sidebar.")
    else:
        # 4. Make the call to your Render API
        headers = {"x-api-key": user_key}
        params = {"number": number_input}
        
        with st.spinner("Connecting to Render API..."):
            try:
                response = requests.get(API_URL, headers=headers, params=params)
                
                if response.status_code == 200:
                    result = response.json().get("result")
                    st.balloons()
                    st.success(f"Calculation Successful!")
                    st.metric(label="Processed Result", value=f"{result:.2f}")
                elif response.status_code == 401:
                    st.error("Invalid API Key. Access Denied.")
                elif response.status_code == 403:
                    st.error("Key is disabled or expired.")
                else:
                    st.error(f"Error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Could not connect to API: {e}")

st.divider()
st.caption("Powered by Neon SQL and Render Cloud.")