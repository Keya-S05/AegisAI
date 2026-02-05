import streamlit as st
import requests

st.set_page_config(page_title="AegisAI Security Dashboard", layout="centered")

st.title("AegisAI – AI Security Monitoring Dashboard")

st.write("Analyze prompts for malicious intent and abnormal AI behavior.")

prompt = st.text_area("Enter prompt to analyze", height=120)

if st.button("Analyze"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"text": prompt},
                timeout=30
            )

            data = response.json()

            st.subheader("Analysis Result")

            st.json(data)

            if data["input_anomaly"]["is_anomaly"]:
                st.error("Input anomaly detected!")
            else:
                st.success("Input looks normal")

            if data["output_behavior"]["output_anomaly"]:
                st.error("Output behavior anomaly detected!")
            else:
                st.success("Output behavior normal")

        except Exception as e:
            st.error(f"Backend not reachable: {e}")

