import pickle
import numpy as np

from app.services.distilbert_engine import (
    semantic_phishing_check
)

from app.services.virustotal_service import (
    get_virustotal_report
)

# ---------------------------------------------------
# LOAD MODELS
# ---------------------------------------------------

lgb_model = pickle.load(
    open("models/lgb_model_small.pkl", "rb")
)

rf_model = pickle.load(
    open("models/rf_model.pkl", "rb")
)

scaler = pickle.load(
    open("models/scaler.pkl", "rb")
)

# ---------------------------------------------------
# HYBRID AI FUSION ENGINE
# ---------------------------------------------------

def fusion_predict(
    url,
    manual_features
):

    # ---------------------------------------------------
    # SCALE FEATURES
    # ---------------------------------------------------

    features_scaled = scaler.transform(
        [manual_features]
    )

    # ---------------------------------------------------
    # LIGHTGBM
    # ---------------------------------------------------

    lgb_prob = float(

        lgb_model.predict_proba(
            features_scaled
        )[0][1]
    )

    # ---------------------------------------------------
    # RANDOM FOREST
    # ---------------------------------------------------

    rf_prob = float(

        rf_model.predict_proba(
            features_scaled
        )[0][1]
    )

    # ---------------------------------------------------
    # DISTILBERT
    # ---------------------------------------------------

    bert_result = semantic_phishing_check(
        url
    )

    bert_prob = float(
        bert_result["confidence"]
    )

    bert_reasons = bert_result["reasons"]

    # ---------------------------------------------------
    # VIRUSTOTAL
    # ---------------------------------------------------

    vt_result = get_virustotal_report(
        url
    )

    vt_prob = float(
        vt_result.get(
            "confidence",
            0.0
        )
    )

    # ---------------------------------------------------
    # INITIAL AI FUSION
    # ---------------------------------------------------

    hybrid_probability = (

        (0.40 * lgb_prob) +

        (0.25 * rf_prob) +

        (0.20 * bert_prob) +

        (0.15 * vt_prob)
    )

    # ---------------------------------------------------
    # SMART URL HEURISTICS
    # ---------------------------------------------------

    suspicious_terms = [

        "login",
        "verify",
        "secure",
        "update",
        "bank",
        "wallet",
        "signin",
        "account",
        "billing",
        "paypal",
        "amazon",
        "otp",
        "confirm",
        "authenticate",
        "support",
        "recovery"
    ]

    lowered_url = url.lower()

    keyword_hits = sum(

        term in lowered_url

        for term in suspicious_terms
    )

    # ---------------------------------------------------
    # PHISHING KEYWORD BOOST
    # ---------------------------------------------------

    if keyword_hits >= 3:

        hybrid_probability += 0.08

    elif keyword_hits == 2:

        hybrid_probability += 0.05

    # ---------------------------------------------------
    # DOMAIN TRICKS
    # ---------------------------------------------------

    if "@" in url:

        hybrid_probability += 0.08

    if "-" in url:

        hybrid_probability += 0.03

    if url.count(".") >= 4:

        hybrid_probability += 0.08

    # ---------------------------------------------------
    # SUSPICIOUS TLDs
    # ---------------------------------------------------

    suspicious_tlds = [

        ".xyz",
        ".ru",
        ".tk",
        ".ml",
        ".ga",
        ".cf",
        ".gq"
    ]

    if any(

        lowered_url.endswith(tld)

        for tld in suspicious_tlds
    ):

        hybrid_probability += 0.10

    # ---------------------------------------------------
    # HTTPS BONUS
    # ---------------------------------------------------

    if lowered_url.startswith(
        "https://"
    ):

        hybrid_probability -= 0.03

    # ---------------------------------------------------
    # TRUSTED DOMAINS
    # ---------------------------------------------------

    trusted_keywords = [

        "google.com",
        "github.com",
        "microsoft.com",
        "openai.com"
    ]

    if any(

        trusted in lowered_url

        for trusted in trusted_keywords
    ):

        hybrid_probability -= 0.15

    # ---------------------------------------------------
    # VIRUSTOTAL BOOST
    # ---------------------------------------------------

    if vt_result.get(
        "status"
    ) == "malicious":

        hybrid_probability += 0.20

    # ---------------------------------------------------
    # CLAMP
    # ---------------------------------------------------

    hybrid_probability = np.clip(

        hybrid_probability,

        0.0,

        1.0
    )

    # ---------------------------------------------------
    # AI REASONS
    # ---------------------------------------------------

    ai_reasons = []

    # ---------------------------------------------------
    # HYBRID SCORE
    # ---------------------------------------------------

    if hybrid_probability >= 0.90:

        ai_reasons.append(
            "Critical phishing probability detected"
        )

    elif hybrid_probability >= 0.75:

        ai_reasons.append(
            "High-risk phishing indicators detected"
        )

    elif hybrid_probability >= 0.50:

        ai_reasons.append(
            "Moderate suspicious activity detected"
        )

    # ---------------------------------------------------
    # LIGHTGBM
    # ---------------------------------------------------

    if lgb_prob >= 0.80:

        ai_reasons.append(
            "LightGBM detected phishing URL patterns"
        )

    # ---------------------------------------------------
    # RF
    # ---------------------------------------------------

    if rf_prob >= 0.80:

        ai_reasons.append(
            "Random Forest detected malicious structure"
        )

    # ---------------------------------------------------
    # DISTILBERT
    # ---------------------------------------------------

    ai_reasons.extend(
        bert_reasons
    )

    # ---------------------------------------------------
    # VIRUSTOTAL SIGNALS
    # ---------------------------------------------------

    if vt_result.get(
        "status"
    ) == "malicious":

        ai_reasons.append(
            f"VirusTotal flagged URL using "
            f"{vt_result.get('malicious', 0)} engines"
        )

    # ---------------------------------------------------
    # URL SIGNALS
    # ---------------------------------------------------

    if keyword_hits >= 2:

        ai_reasons.append(
            "Multiple phishing-related keywords detected"
        )

    if any(

        lowered_url.endswith(tld)

        for tld in suspicious_tlds
    ):

        ai_reasons.append(
            "Suspicious domain extension detected"
        )

    # ---------------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------------

    ai_reasons = list(
        set(ai_reasons)
    )

    # ---------------------------------------------------
    # FINAL RETURN
    # ---------------------------------------------------

    return {

        "probability": round(
            float(hybrid_probability),
            4
        ),

        "lgb_prob": round(
            lgb_prob,
            4
        ),

        "rf_prob": round(
            rf_prob,
            4
        ),

        "bert_prob": round(
            bert_prob,
            4
        ),

        "vt_prob": round(
            vt_prob,
            4
        ),

        "vt_status": vt_result.get(
            "status",
            "unknown"
        ),

        "vt_engines": vt_result.get(
            "malicious",
            0
        ),

        "reasons": ai_reasons
    }