import pickle
import numpy as np

from app.services.distilbert_engine import (
    semantic_phishing_check
)

from app.services.virustotal_engine import (
    get_virustotal_report
)

# ---------------------------------------------------
# LOAD MODELS
# ---------------------------------------------------

lgb_model = pickle.load(
    open("models/lgb_model_small.pkl", "rb")
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
    # RF REMOVED
    # ---------------------------------------------------

    rf_prob = lgb_prob

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
    # HYBRID FUSION
    # ---------------------------------------------------

    hybrid_probability = (

        (0.10 * lgb_prob) +

        (0.50 * bert_prob) +

        (0.40 * vt_prob)

    )

    # ---------------------------------------------------
    # URL ANALYSIS
    # ---------------------------------------------------

    lowered_url = url.lower()

    suspicious_terms = [

        "login",
        "verify",
        "secure",
        "signin",
        "account",
        "billing",
        "otp",
        "confirm",
        "authenticate",
        "recovery"

    ]

    keyword_hits = sum(

        term in lowered_url

        for term in suspicious_terms

    )

    if keyword_hits >= 3:

        hybrid_probability += 0.08

    elif keyword_hits == 2:

        hybrid_probability += 0.05

    # ---------------------------------------------------
    # DOMAIN TRICKS
    # ---------------------------------------------------

    if "@" in lowered_url:

        hybrid_probability += 0.08

    if lowered_url.count("-") >= 3:

        hybrid_probability += 0.05

    if lowered_url.count(".") >= 4:

        hybrid_probability += 0.08

    # ---------------------------------------------------
    # SUSPICIOUS TLDS
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

        hybrid_probability -= 0.05

    # ---------------------------------------------------
    # TRUSTED DOMAINS
    # ---------------------------------------------------

    trusted_domains = [

        "google.com",
        "github.com",
        "openai.com",
        "youtube.com",
        "amazon.com",
        "linkedin.com",
        "stackoverflow.com",
        "wikipedia.org",
        "microsoft.com"

    ]

    if any(

        trusted in lowered_url

        for trusted in trusted_domains

    ):

        hybrid_probability -= 0.40

    # ---------------------------------------------------
    # VT BOOST
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
    # REASONS
    # ---------------------------------------------------

    ai_reasons = []

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

    if lgb_prob >= 0.80:

        ai_reasons.append(
            "LightGBM detected phishing URL patterns"
        )

    ai_reasons.extend(
        bert_reasons
    )

    if vt_result.get(
        "status"
    ) == "malicious":

        ai_reasons.append(
            f"VirusTotal flagged URL using {vt_result.get('malicious',0)} engines"
        )

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

    ai_reasons = list(
        set(ai_reasons)
    )

    # ---------------------------------------------------
    # RETURN
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