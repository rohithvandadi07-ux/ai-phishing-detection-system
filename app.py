from fastapi import FastAPI
import pickle
from urllib.parse import urlparse

from utils.features import extract_features
from utils.explain import explain_url
from utils.reputation import analyze_url_reputation

from utils.threat_intel import (
    check_virustotal,
    check_phishtank
)

app = FastAPI()

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

lgb_model = pickle.load(open("models/lgb_model_small.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

# ---------------------------------------------------
# TRUSTED SAFE DOMAINS
# ---------------------------------------------------

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

# ---------------------------------------------------
# HOME ROUTE
# ---------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Phishing Detection API Running"
    }

# ---------------------------------------------------
# MAIN PREDICTION ROUTE
# ---------------------------------------------------

@app.post("/predict")
def predict(url: str):

    try:

        # ---------------------------------------------------
        # DOMAIN PARSING
        # ---------------------------------------------------

        parsed = urlparse(url)
        hostname = parsed.netloc.lower()

        if hostname.startswith("www."):
            hostname = hostname[4:]

        # ---------------------------------------------------
        # SAFE DOMAIN WHITELIST
        # ---------------------------------------------------

        if hostname in SAFE_DOMAINS:

            return {

                "prediction": "safe",
                "confidence": 1.0,
                "risk_score": 0,
                "risk_level": "SAFE",
                "reasons": [
                    "Trusted domain whitelist"
                ]

            }

        # ---------------------------------------------------
        # FEATURE EXTRACTION
        # ---------------------------------------------------

        feat = extract_features(url)
        feat_scaled = scaler.transform([feat])

        # ---------------------------------------------------
        # ML PREDICTION
        # ---------------------------------------------------

        pred = lgb_model.predict(feat_scaled)[0]

        prob = float(
            lgb_model.predict_proba(feat_scaled)[0][1]
        )

        # ---------------------------------------------------
        # INITIAL EXPLANATIONS
        # ---------------------------------------------------

        reasons = list(set(explain_url(url)))

        # ---------------------------------------------------
        # VIRUSTOTAL CHECK
        # ---------------------------------------------------

        vt_result = check_virustotal(url)

        if vt_result["malicious"]:

            reasons.append(
                f"Flagged by VirusTotal ({vt_result['detections']} detections)"
            )

        # ---------------------------------------------------
        # PHISHTANK / OPENPHISH CHECK
        # ---------------------------------------------------

        pt_result = check_phishtank(url)

        if pt_result["malicious"]:

            reasons.append(
                "Flagged by PhishTank database"
            )

        # ---------------------------------------------------
        # URL REPUTATION ENGINE
        # ---------------------------------------------------

        reputation_result = analyze_url_reputation(url)

        reasons.extend(
            reputation_result["indicators"]
        )

        # Remove duplicates
        reasons = list(set(reasons))

        # ---------------------------------------------------
        # RISK SCORE ENGINE
        # ---------------------------------------------------

        risk_score = 0

        # ML contribution
        risk_score += int(prob * 45)

        # Explanations contribution
        risk_score += len(reasons) * 6

        # Reputation engine contribution
        risk_score += reputation_result["score"]

        # VirusTotal contribution
        if vt_result["malicious"]:
            risk_score += 25

        # PhishTank contribution
        if pt_result["malicious"]:
            risk_score += 20

        # ---------------------------------------------------
        # EXTRA SUSPICIOUS KEYWORD ANALYSIS
        # ---------------------------------------------------

        suspicious_keywords = [

            "login",
            "secure",
            "verify",
            "update",
            "bank",
            "paypal",
            "signin",
            "account",
            "password",
            "auth"

        ]

        lower_url = url.lower()

        for word in suspicious_keywords:

            if word in lower_url:

                risk_score += 4

        # ---------------------------------------------------
        # URL LENGTH CHECK
        # ---------------------------------------------------

        if len(url) > 75:

            reasons.append("Very long URL")
            risk_score += 10

        # ---------------------------------------------------
        # SCORE CLAMP
        # ---------------------------------------------------

        if risk_score > 100:
            risk_score = 100

        # ---------------------------------------------------
        # RISK LEVELS
        # ---------------------------------------------------

        if risk_score >= 80:

            risk_level = "CRITICAL"

        elif risk_score >= 60:

            risk_level = "HIGH"

        elif risk_score >= 35:

            risk_level = "MEDIUM"

        else:

            risk_level = "SAFE"

        # ---------------------------------------------------
        # FINAL PREDICTION
        # ---------------------------------------------------

        prediction = "malicious" if risk_level != "SAFE" else "safe"

        # ---------------------------------------------------
        # FINAL RESPONSE
        # ---------------------------------------------------

        return {

            "prediction": prediction,
            "confidence": round(prob, 4),
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
            "reasons": [
                str(e)
            ]

        }