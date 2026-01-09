import pickle
import re
import streamlit as st

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🛡️ Phishing Website Detector")
st.write(
    "Enter a website URL and I’ll predict whether "
    "it’s likely phishing."
)

url = st.text_input("Enter website URL")


def extract_features(url: str):
    features = {}
    features["url_length"] = len(url)
    features["has_at"] = int("@" in url)
    features["has_https"] = int(url.startswith("https"))
    features["contains_ip"] = int(
        bool(re.match(r"(\d{1,3}\.){3}\d{1,3}", url))
    )
    features["digits_count"] = sum(c.isdigit() for c in url)

    return list(features.values())


if st.button("Check"):
    if not url.strip():
        st.warning("Please enter a URL first.")
    else:
        feats = [extract_features(url)]
        result = model.predict(feats)[0]

        if result == 1:
            st.error("🚨 This website might be **PHISHING**!")
        else:
            st.success("✅ Looks **safe** — but always stay cautious.")
