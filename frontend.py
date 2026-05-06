import streamlit as st
import requests

st.set_page_config(page_title="Phishing Detector")

st.title("🔴 Real-Time Phishing Detection System")

# Always show input
url = st.text_input("Enter URL")

# Always show button
check = st.button("Check URL")

if check:
    if url:
        try:
            res = requests.post(
                "http://127.0.0.1:8000/predict",
                params={"url": url}
            )

            data = res.json()

            if data["prediction"] == "malicious":
                if data["confidence"] > 0.8:
                    st.error("⚠️ Malicious URL detected!")
                else:
                    st.warning("⚠️ Suspicious URL (low confidence)")
            else:
                st.success("✅ Safe URL")

            st.write(f"Confidence: {data['confidence']:.4f}")

            st.write("### Why flagged?")
            for reason in data["why_flagged"]:
                st.write(f"- {reason}")

        except:
            st.error("❌ API not reachable. Start FastAPI server.")
    else:
        st.warning("⚠️ Please enter a URL")