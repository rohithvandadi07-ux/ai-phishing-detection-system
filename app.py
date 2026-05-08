from fastapi import FastAPI
import pickle
from urllib.parse import urlparse

from utils.features import extract_features
from utils.explain import explain_url

app = FastAPI()

# Load ML model
lgb_model = pickle.load(open("models/lgb_model_small.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

# Trusted domains
SAFE_DOMAINS = {
    "google.com",
    "github.com",
    "amazon.com",
    "amazon.in",
    "microsoft.com",
    "apple.com",
    "linkedin.com",
    "stackoverflow.com"
}


@app.get("/")
def home():
    return {"message": "AI Phishing Detection API Running"}


@app.post("/predict")
def predict(url: str):

    try:

        parsed = urlparse(url)
        hostname = parsed.netloc.lower()

        if hostname.startswith("www."):
            hostname = hostname[4:]

        # SAFE DOMAIN OVERRIDE
        if hostname in SAFE_DOMAINS:

            return {
                "prediction": "safe",
                "confidence": 1.0,
                "risk_score": 0,
                "risk_level": "SAFE",
                "reasons": ["Trusted domain whitelist"]
            }

        # Extract features
        feat = extract_features(url)
        feat_scaled = scaler.transform([feat])

        # ML prediction
        pred = lgb_model.predict(feat_scaled)[0]
        prob = float(lgb_model.predict_proba(feat_scaled)[0][1])

        # AI explanations
        reasons = explain_url(url)

        # -------------------------
        # RISK SCORE ENGINE
        # -------------------------

        risk_score = 0

        # ML confidence contribution
        risk_score += int(prob * 60)

        # Explanation contribution
        risk_score += len(reasons) * 10

        # Bonus penalties
        suspicious_keywords = [
            "login",
            "secure",
            "verify",
            "update",
            "bank",
            "paypal",
            "signin"
        ]

        lower_url = url.lower()

        for word in suspicious_keywords:
            if word in lower_url:
                risk_score += 5

        # Clamp
        if risk_score > 100:
            risk_score = 100

        # -------------------------
        # RISK LEVELS
        # -------------------------

        if risk_score >= 80:
            risk_level = "CRITICAL"

        elif risk_score >= 60:
            risk_level = "HIGH"

        elif risk_score >= 35:
            risk_level = "MEDIUM"

        else:
            risk_level = "SAFE"

        # Final prediction logic
        prediction = "malicious" if risk_level != "SAFE" else "safe"

        return {

            "prediction": prediction,
            "confidence": prob,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "reasons": reasons
        }

    except Exception as e:

        return {
            "prediction": "error",
            "confidence": 0.0,
            "risk_score": 0,
            "risk_level": "UNKNOWN",
            "reasons": [str(e)]
        }