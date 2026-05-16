import pickle

from app.services.distilbert_engine import (
    semantic_phishing_check
)

# ---------------------------------------------------
# LOAD LIGHTGBM MODEL
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

def fusion_predict(url, manual_features):

    # ---------------------------------------------------
    # SCALE FEATURES
    # ---------------------------------------------------

    features_scaled = scaler.transform(
        [manual_features]
    )

    # ---------------------------------------------------
    # LIGHTGBM PREDICTION
    # ---------------------------------------------------

    lgb_prob = float(

        lgb_model.predict_proba(
            features_scaled
        )[0][1]

    )

    # ---------------------------------------------------
    # DISTILBERT ANALYSIS
    # ---------------------------------------------------

    bert_result = semantic_phishing_check(url)

    bert_prob = float(
        bert_result["confidence"]
    )

    bert_reasons = bert_result["reasons"]

    # ---------------------------------------------------
    # HYBRID FUSION
    # ---------------------------------------------------

    hybrid_probability = (

        (0.80 * lgb_prob) +

        (0.20 * bert_prob)

    )

    # ---------------------------------------------------
    # CLAMP VALUE
    # ---------------------------------------------------

    hybrid_probability = min(
        max(hybrid_probability, 0.0),
        1.0
    )

    # ---------------------------------------------------
    # AI REASONS
    # ---------------------------------------------------

    ai_reasons = []

    if hybrid_probability >= 0.80:

        ai_reasons.append(
            "Hybrid AI engine flagged high-risk phishing indicators"
        )

    elif hybrid_probability >= 0.60:

        ai_reasons.append(
            "Hybrid AI engine detected suspicious phishing behavior"
        )

    elif hybrid_probability >= 0.40:

        ai_reasons.append(
            "Hybrid AI engine detected moderate suspicious activity"
        )

    # ---------------------------------------------------
    # LIGHTGBM SIGNALS
    # ---------------------------------------------------

    if lgb_prob >= 0.80:

        ai_reasons.append(
            "LightGBM detected phishing patterns"
        )

    # ---------------------------------------------------
    # DISTILBERT SIGNALS
    # ---------------------------------------------------

    ai_reasons.extend(
        bert_reasons
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
            hybrid_probability,
            4
        ),

        "lgb_prob": round(
            lgb_prob,
            4
        ),

        "bert_prob": round(
            bert_prob,
            4
        ),

        "rf_prob": 0.0,

        "reasons": ai_reasons

    }