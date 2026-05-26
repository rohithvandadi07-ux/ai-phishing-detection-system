from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

import time
import re
import math

from urllib.parse import urlparse

from sqlalchemy.orm import Session

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
# DATABASE
# ---------------------------------------------------

from app.database.database import (
    get_db,
    log_detection
)

from app.database.models import (
    ScanHistory
)

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
# VIRUSTOTAL
# ---------------------------------------------------

from app.services.virustotal_engine import (
    get_virustotal_report
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
# REPUTATION ENGINE
# ---------------------------------------------------

from app.services.reputation_engine import (
    analyze_reputation
)

# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

router = APIRouter()

# ---------------------------------------------------
# SUSPICIOUS KEYWORDS
# ---------------------------------------------------

SUSPICIOUS_KEYWORDS = [

    "login",
    "verify",
    "secure",
    "account",
    "update",
    "bank",
    "paypal",
    "amazon",
    "wallet",
    "signin",
    "password",
    "otp",
    "billing",
    "crypto",
    "gift",
    "microsoft",
    "google",
    "apple"

]

# ---------------------------------------------------
# SUSPICIOUS TLDS
# ---------------------------------------------------

SUSPICIOUS_TLDS = [

    ".xyz",
    ".top",
    ".ru",
    ".tk",
    ".gq",
    ".ml",
    ".cf",
    ".ga"

]

# ---------------------------------------------------
# URL ENTROPY
# ---------------------------------------------------

def calculate_entropy(text):

    prob = [

        float(text.count(c)) / len(text)

        for c in dict.fromkeys(list(text))

    ]

    entropy = -sum(

        p * math.log(p) / math.log(2.0)

        for p in prob

    )

    return entropy

# ---------------------------------------------------
# ADVANCED URL ANALYSIS
# ---------------------------------------------------

def advanced_url_analysis(url):

    score = 0

    indicators = []

    lower_url = url.lower()

    # ------------------------------------------------
    # KEYWORDS
    # ------------------------------------------------

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in lower_url:

            score += 8

            indicators.append(
                f"Suspicious keyword detected: {keyword}"
            )

    # ------------------------------------------------
    # LONG URL
    # ------------------------------------------------

    if len(url) > 75:

        score += 10

        indicators.append(
            "Unusually long URL detected"
        )

    # ------------------------------------------------
    # @ SYMBOL
    # ------------------------------------------------

    if "@" in url:

        score += 15

        indicators.append(
            "@ symbol obfuscation detected"
        )

    # ------------------------------------------------
    # MULTIPLE HYPHENS
    # ------------------------------------------------

    if url.count("-") >= 3:

        score += 12

        indicators.append(
            "Multiple hyphens detected"
        )

    # ------------------------------------------------
    # IP ADDRESS
    # ------------------------------------------------

    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"

    if re.search(ip_pattern, url):

        score += 20

        indicators.append(
            "IP address URL detected"
        )

    # ------------------------------------------------
    # SUSPICIOUS TLD
    # ------------------------------------------------

    for tld in SUSPICIOUS_TLDS:

        if lower_url.endswith(tld):

            score += 15

            indicators.append(
                f"Suspicious TLD detected: {tld}"
            )

    # ------------------------------------------------
    # ENTROPY
    # ------------------------------------------------

    entropy = calculate_entropy(url)

    if entropy > 4.2:

        score += 10

        indicators.append(
            "High entropy random-looking URL"
        )

    # ------------------------------------------------
    # TOO MANY SUBDOMAINS
    # ------------------------------------------------

    if url.count(".") >= 4:

        score += 10

        indicators.append(
            "Too many subdomains detected"
        )

    return {

        "score": score,

        "indicators": indicators

    }

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

    body: URLRequest,

    db: Session = Depends(get_db)

):

    start_time = time.time()

    url = body.url.strip()

    try:

        logger.info(
            f"Scanning URL: {url}"
        )

        # ---------------------------------------------------
        # VALIDATION
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
        # CACHE
        # ---------------------------------------------------

        cached = get_cached_result(url)

        if cached:

            cached["cached"] = True

            return cached

        # ---------------------------------------------------
        # FEATURE EXTRACTION
        # ---------------------------------------------------

        feat = extract_features(url)

        # ---------------------------------------------------
        # HEURISTICS
        # ---------------------------------------------------

        heuristic_result = advanced_url_analysis(url)

        heuristic_score = heuristic_result["score"]

        heuristic_indicators = heuristic_result["indicators"]

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

        bert_prob = fusion_result["bert_prob"]

        # ---------------------------------------------------
        # BOOST HEURISTICS
        # ---------------------------------------------------

        prob += (heuristic_score / 100) * 0.25

        prob = min(prob, 1.0)

        # ---------------------------------------------------
        # DISTILBERT
        # ---------------------------------------------------

        semantic_result = semantic_phishing_check(url)

        semantic_score = semantic_result["score"]

        semantic_confidence = semantic_result["confidence"]

        semantic_reasons = semantic_result["reasons"]

        # ---------------------------------------------------
        # REASONS
        # ---------------------------------------------------

        reasons = list(
            set(explain_url(url))
        )

        reasons.extend(semantic_reasons)

        reasons.extend(heuristic_indicators)

        # ---------------------------------------------------
        # WHOIS
        # ---------------------------------------------------

        whois_result = analyze_domain(url)

        reasons.extend(
            whois_result["indicators"]
        )

        # ---------------------------------------------------
        # REPUTATION
        # ---------------------------------------------------

        reputation_result = analyze_reputation(
            url
        )

        reputation_score = reputation_result[
            "reputation_score"
        ]

        reputation_level = reputation_result[
            "reputation_level"
        ]

        reasons.extend(
            reputation_result["indicators"]
        )

        # ---------------------------------------------------
        # VIRUSTOTAL
        # ---------------------------------------------------

        vt_result = get_virustotal_report(url)

        if vt_result["status"] == "malicious":

            reasons.append(

                f"VirusTotal detected malware ({vt_result['malicious']} engines flagged)"

            )

            prob += 0.20

        elif vt_result["status"] == "suspicious":

            reasons.append(
                "VirusTotal marked URL as suspicious"
            )

            prob += 0.10

        elif vt_result["status"] == "submitted":

            reasons.append(
                "URL submitted to VirusTotal"
            )

        elif vt_result["status"] == "rate_limited":

            reasons.append(
                "VirusTotal API limit reached"
            )

        # ---------------------------------------------------
        # REMOVE DUPLICATES
        # ---------------------------------------------------

        reasons = list(set(reasons))

        # ---------------------------------------------------
        # RISK SCORE
        # ---------------------------------------------------

        risk_score = int(prob * 100)

        risk_score += int(
            reputation_score * 0.35
        )

        risk_score += int(
            whois_result["score"] * 0.25
        )

        if vt_result["status"] == "malicious":

            risk_score += 20

        if heuristic_score >= 40:

            risk_score = max(
                risk_score,
                90
            )

        risk_score = min(
            risk_score,
            100
        )

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
        # RESPONSE
        # ---------------------------------------------------

        inference_time = round(
            time.time() - start_time,
            4
        )

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

                "bert_probability":
                    round(bert_prob, 4),

                "hybrid_probability":
                    round(prob, 4),

                "semantic_score":
                    semantic_score,

                "semantic_confidence":
                    semantic_confidence,

                "heuristic_score":
                    heuristic_score,

                "reputation_score":
                    reputation_score,

                "reputation_level":
                    reputation_level,

                "whois_score":
                    whois_result["score"],

                "virustotal":
                    vt_result
            }
        }

        # ---------------------------------------------------
        # CACHE
        # ---------------------------------------------------

        store_result(
            url,
            result
        )

        # ---------------------------------------------------
        # DATABASE
        # ---------------------------------------------------

        history = ScanHistory(

            url=url,

            prediction=prediction,

            risk_score=risk_score,

            risk_level=risk_level,

            confidence=round(prob, 4)

        )

        db.add(history)

        db.commit()

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