from fastapi import APIRouter
import asyncio
import time

from urllib.parse import urlparse

from app.schemas.request_models import URLRequest

from app.utils.features import extract_features

from app.services.explain import explain_url

from app.utils.cache import (
    get_cached_result,
    store_result
)

from app.utils.async_scanner import async_scan

from app.database.database import (
    log_detection
)

from app.services.fusion_engine import (
    fusion_predict
)

from app.utils.whois_intel import (
    analyze_domain
)

from app.services.distilbert_engine import (
    semantic_phishing_check
)

from app.core.logger import logger

# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

router = APIRouter()

# ---------------------------------------------------
# SAFE DOMAINS
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
# PREDICT ROUTE
# ---------------------------------------------------

@router.post("/predict")

def predict(request: URLRequest):

    start_time = time.time()

    url = request.url

    try:

        logger.info(f"Scanning URL: {url}")

        # ---------------------------------------------------
        # CACHE CHECK
        # ---------------------------------------------------

        cached = get_cached_result(url)

        if cached:

            cached["cached"] = True

            return cached

        # ---------------------------------------------------
        # DOMAIN PARSING
        # ---------------------------------------------------

        parsed = urlparse(url)

        hostname = parsed.netloc.lower()

        if hostname.startswith("www."):

            hostname = hostname[4:]

        # ---------------------------------------------------
        # SAFE WHITELIST
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

            return result

        # ---------------------------------------------------
        # FEATURE EXTRACTION
        # ---------------------------------------------------

        feat = extract_features(url)

        # ---------------------------------------------------
        # HYBRID ENGINE
        # ---------------------------------------------------

        fusion_result = fusion_predict(

            url,
            feat

        )

        prob = fusion_result["probability"]

        lgb_prob = fusion_result["lgb_prob"]

        rf_prob = fusion_result["rf_prob"]

        # ---------------------------------------------------
        # DISTILBERT
        # ---------------------------------------------------

        semantic_result = semantic_phishing_check(url)

        semantic_score = semantic_result["score"]

        semantic_confidence = semantic_result["confidence"]

        semantic_reasons = semantic_result["reasons"]

        # ---------------------------------------------------
        # EXPLANATIONS
        # ---------------------------------------------------

        reasons = list(

            set(explain_url(url))

        )

        reasons.extend(

            semantic_reasons

        )

        # ---------------------------------------------------
        # ASYNC SCAN
        # ---------------------------------------------------

        scan_results = asyncio.run(

            async_scan(

                url,
                run_bert_model=False

            )

        )

        # ---------------------------------------------------
        # VT
        # ---------------------------------------------------

        vt_result = scan_results["virustotal"]

        if vt_result["malicious"]:

            reasons.append(

                f"Flagged by VirusTotal ({vt_result['detections']} detections)"

            )

        # ---------------------------------------------------
        # FINAL SCORE
        # ---------------------------------------------------

        risk_score = int(prob * 100)

        if risk_score > 100:

            risk_score = 100

        # ---------------------------------------------------
        # RISK LEVEL
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

        prediction = (

            "malicious"

            if risk_level != "SAFE"

            else "safe"

        )

        # ---------------------------------------------------
        # INFERENCE TIME
        # ---------------------------------------------------

        inference_time = round(

            time.time() - start_time,
            4

        )

        # ---------------------------------------------------
        # FINAL RESPONSE
        # ---------------------------------------------------

        result = {

            "prediction": prediction,

            "confidence": round(prob, 4),

            "risk_score": risk_score,

            "risk_level": risk_level,

            "inference_time": inference_time,

            "reasons": reasons,

            "ai_engine": {

                "lgb_probability":

                    round(lgb_prob, 4),

                "rf_probability":

                    round(rf_prob, 4),

                "semantic_score":

                    semantic_score,

                "semantic_confidence":

                    semantic_confidence

            }

        }

        # ---------------------------------------------------
        # CACHE STORE
        # ---------------------------------------------------

        store_result(

            url,
            result

        )

        # ---------------------------------------------------
        # DATABASE LOGGING
        # ---------------------------------------------------

        log_detection(

            url=url,

            prediction=prediction,

            risk_score=risk_score,

            risk_level=risk_level,

            confidence=round(prob, 4)

        )

        logger.info(

            f"{url} -> {prediction}"

        )

        return result

    except Exception as e:

        logger.error(str(e))

        return {

            "prediction": "error",

            "confidence": 0.0,

            "risk_score": 0,

            "risk_level": "UNKNOWN",

            "reasons": [

                str(e)

            ]

        }