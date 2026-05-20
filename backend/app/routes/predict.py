from fastapi import APIRouter, Request
import asyncio
import time

from urllib.parse import urlparse

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

from app.core.config import settings

# ---------------------------------------------------
# CONSTANTS
# ---------------------------------------------------

from app.core.constants import *

# ---------------------------------------------------
# RATE LIMITER
# ---------------------------------------------------

from app.core.rate_limiter import limiter

# ---------------------------------------------------
# LOGGER
# ---------------------------------------------------

from app.core.logger import logger

# ---------------------------------------------------
# SCHEMAS
# ---------------------------------------------------

from app.schemas.request_models import URLRequest

from app.schemas.response_models import (
    PredictionResponse
)

# ---------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------

from app.utils.features import extract_features

# ---------------------------------------------------
# EXPLAINABILITY
# ---------------------------------------------------

from app.services.explain import explain_url

# ---------------------------------------------------
# CACHE
# ---------------------------------------------------

from app.utils.cache import (
    get_cached_result,
    store_result
)

# ---------------------------------------------------
# ASYNC SCANNER
# ---------------------------------------------------

from app.utils.async_scanner import async_scan

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

from app.database.database import (
    log_detection
)

# ---------------------------------------------------
# AI ENGINES
# ---------------------------------------------------

from app.services.fusion_engine import (
    fusion_predict
)

from app.services.distilbert_engine import (
    semantic_phishing_check
)

# ---------------------------------------------------
# WHOIS
# ---------------------------------------------------

from app.utils.whois_intel import (
    analyze_domain
)

# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

router = APIRouter()

# ---------------------------------------------------
# PREDICTION ROUTE
# ---------------------------------------------------

@limiter.limit("20/minute")

@router.post(

    "/predict",

    response_model=PredictionResponse,

    tags=["Prediction"]

)

def predict(

    request: Request,

    body: URLRequest

):

    start_time = time.time()

    # ---------------------------------------------------
    # SANITIZE URL
    # ---------------------------------------------------

    url = body.url.strip()

    try:

        logger.info(f"Scanning URL: {url}")

        # ---------------------------------------------------
        # URL VALIDATION
        # ---------------------------------------------------

        if not (

            url.startswith("http://")

            or

            url.startswith("https://")

        ):

            return {

                "prediction": PREDICTION_ERROR,

                "confidence": 0.0,

                "risk_score": 0,

                "risk_level": RISK_HIGH,

                "inference_time": 0.0,

                "reasons": [

                    "Invalid URL format"

                ],

                "ai_engine": {}

            }

        # ---------------------------------------------------
        # URL LENGTH VALIDATION
        # ---------------------------------------------------

        if len(url) > MAX_URL_LENGTH:

            return {

                "prediction": PREDICTION_ERROR,

                "confidence": 0.0,

                "risk_score": 0,

                "risk_level": RISK_HIGH,

                "inference_time": 0.0,

                "reasons": [

                    "URL exceeds maximum allowed length"

                ],

                "ai_engine": {}

            }

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
        # SAFE DOMAIN WHITELIST
        # ---------------------------------------------------

        if hostname in settings.SAFE_DOMAINS:

            result = {

                "prediction": PREDICTION_SAFE,

                "confidence": 1.0,

                "risk_score": 0,

                "risk_level": RISK_SAFE,

                "inference_time": 0.0,

                "reasons": [

                    "Trusted domain whitelist"

                ],

                "ai_engine": {}

            }

            return result

        # ---------------------------------------------------
        # FEATURE EXTRACTION
        # ---------------------------------------------------

        feat = extract_features(url)

        # ---------------------------------------------------
        # HYBRID AI ENGINE
        # ---------------------------------------------------

        fusion_result = fusion_predict(

            url,
            feat

        )

        prob = fusion_result["probability"]

        lgb_prob = fusion_result["lgb_prob"]

        rf_prob = fusion_result["rf_prob"]

        # ---------------------------------------------------
        # DISTILBERT ENGINE
        # ---------------------------------------------------

        semantic_result = semantic_phishing_check(url)

        semantic_score = semantic_result["score"]

        semantic_confidence = semantic_result["confidence"]

        semantic_reasons = semantic_result["reasons"]

        # ---------------------------------------------------
        # EXPLAINABILITY
        # ---------------------------------------------------

        reasons = list(

            set(explain_url(url))

        )

        reasons.extend(

            semantic_reasons

        )

        # ---------------------------------------------------
        # WHOIS ANALYSIS
        # ---------------------------------------------------

        whois_result = analyze_domain(url)

        reasons.extend(

            whois_result["indicators"]

        )

        # ---------------------------------------------------
        # ASYNC THREAT SCAN
        # ---------------------------------------------------

        scan_results = asyncio.run(

            async_scan(

                url,
                run_bert_model=False

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
        # REMOVE DUPLICATES
        # ---------------------------------------------------

        reasons = list(

            set(reasons)

        )

        # ---------------------------------------------------
        # RISK SCORE
        # ---------------------------------------------------

        risk_score = int(prob * 100)

        if vt_result["malicious"]:

            risk_score += 20

        if risk_score > 100:

            risk_score = 100

        # ---------------------------------------------------
        # RISK LEVEL
        # ---------------------------------------------------

        if risk_score >= CRITICAL_THRESHOLD:

            risk_level = RISK_CRITICAL

        elif risk_score >= HIGH_THRESHOLD:

            risk_level = RISK_HIGH

        elif risk_score >= SAFE_THRESHOLD:

            risk_level = RISK_MEDIUM

        else:

            risk_level = RISK_SAFE

        # ---------------------------------------------------
        # FINAL PREDICTION
        # ---------------------------------------------------

        prediction = (

            PREDICTION_MALICIOUS

            if risk_level != RISK_SAFE

            else PREDICTION_SAFE

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

                "hybrid_probability":

                    round(prob, 4),

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

            "prediction": PREDICTION_ERROR,

            "confidence": 0.0,

            "risk_score": 0,

            "risk_level": RISK_HIGH,

            "inference_time": 0.0,

            "reasons": [

                str(e)

            ],

            "ai_engine": {}

        }