from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
from urllib.parse import urlparse

from utils.features import extract_features
from utils.explain import explain_url

app = FastAPI()

# 🔓 Allow extension/browser requests (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
lgb_model = pickle.load(open("models/lgb_model_small.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

# 🔒 Trusted domains
SAFE_DOMAINS = {
    "google.com", "github.com", "amazon.com", "amazon.in",
    "microsoft.com", "apple.com", "facebook.com",
    "stackoverflow.com", "linkedin.com",
    "youtube.com", "openai.com", "kaggle.com"
}


@app.get("/")
def home():
    return {"message": "API Running"}


@app.post("/predict")
def predict(url: str):
    try:
        # 🚫 Ignore non-web URLs (VERY IMPORTANT)
        if not url.startswith("http"):
            return {
                "prediction": "safe",
                "confidence": 1.0,
                "why_flagged": ["Non-web URL (ignored)"]
            }

        # 🔍 Parse domain
        parsed = urlparse(url)
        hostname = parsed.netloc.lower()

        # remove www.
        if hostname.startswith("www."):
            hostname = hostname[4:]

        # 🔥 SAFE DOMAIN CHECK (supports subdomains)
        if any(hostname == d or hostname.endswith("." + d) for d in SAFE_DOMAINS):
            return {
                "prediction": "safe",
                "confidence": 1.0,
                "why_flagged": ["Trusted domain whitelist"]
            }

        # 🔢 Extract features
        feat = extract_features(url)
        feat_scaled = scaler.transform([feat])

        # 🤖 Model prediction
        pred = lgb_model.predict(feat_scaled)[0]
        prob = lgb_model.predict_proba(feat_scaled)[0][1]

        return {
            "prediction": "malicious" if pred == 1 else "safe",
            "confidence": float(prob),
            "why_flagged": explain_url(url)
        }

    except Exception as e:
        # 🚨 Fail-safe
        return {
            "prediction": "error",
            "confidence": 0.0,
            "why_flagged": [f"Internal error: {str(e)}"]
        }