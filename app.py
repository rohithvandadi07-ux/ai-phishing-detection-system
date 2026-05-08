from fastapi import FastAPI
import pickle
import asyncio
from urllib.parse import urlparse

from utils.features import extract_features
from utils.explain import explain_url

from utils.cache import (
    get_cached_result,
    store_result
)

from utils.async_scanner import async_scan

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
        # CACHE CHECK
        # ---------------------------------------------------

        cached = get_cached_result(url)

        if cached:
            return cached

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

            result = {

                "prediction": "safe",
                "confidence": 1.0,
                "risk_score": 0,
                "risk_level": "SAFE",
                "reasons": [
                    "Trusted domain whitelist"
                ]

            }

            store_result(url, result)

            return result

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
        # FAST RISK ESTIMATION
        # ---------------------------------------------------

        fast_risk = 0

        if prob > 0.80:
            fast_risk += 40

        if len(reasons) >= 3:
            fast_risk += 30

        # ---------------------------------------------------
        # ASYNC SCANNING ENGINE
        # ---------------------------------------------------

        scan_results = asyncio.run(
            async_scan(
                url,
                run_bert_model=fast_risk >= 25
            )
        )

        # ---------------------------------------------------
        # VIRUSTOTAL
        # ---------------------------------------------------

        vt_result = scan_results["virustotal"]

        if vt_result["malicious"]:

            reasons.append(
                f"Flagged by VirusTotal ({vt_result['detections']} detections)"
            )

        # ---------------------------------------------------
        # PHISHTANK
        # ---------------------------------------------------

        pt_result = scan_results["phishtank"]

        if pt_result["malicious"]:

            reasons.append(
                "Flagged by PhishTank database"
            )

        # ---------------------------------------------------
        # REPUTATION ENGINE
        # ---------------------------------------------------

        reputation_result = scan_results["reputation"]

        reasons.extend(
            reputation_result["indicators"]
        )

        # ---------------------------------------------------
        # DOMAIN INTELLIGENCE
        # ---------------------------------------------------

        domain_result = scan_results["domain_intel"]

        reasons.extend(
            domain_result["indicators"]
        )

        # ---------------------------------------------------
        # DISTILBERT ANALYSIS
        # ---------------------------------------------------

        bert_result = scan_results["bert"]

        reasons.extend(
            bert_result["reasons"]
        )

        # ---------------------------------------------------
        # REMOVE DUPLICATES
        # ---------------------------------------------------

        reasons = list(set(reasons))

        # ---------------------------------------------------
        # FINAL RISK SCORE
        # ---------------------------------------------------

        risk_score = 0

        # ML contribution
        risk_score += int(prob * 35)

        # Explanation contribution
        risk_score += len(reasons) * 4

        # Reputation contribution
        risk_score += reputation_result["score"]

        # Domain intelligence contribution
        risk_score += domain_result["score"]

        # DistilBERT contribution
        risk_score += bert_result["score"]

        # VirusTotal contribution
        if vt_result["malicious"]:
            risk_score += 25

        # PhishTank contribution
        if pt_result["malicious"]:
            risk_score += 20

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

        result = {

            "prediction": prediction,
            "confidence": round(prob, 4),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "reasons": reasons

        }

        # ---------------------------------------------------
        # STORE CACHE
        # ---------------------------------------------------

        store_result(url, result)

        return result

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