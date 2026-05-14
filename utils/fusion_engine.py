import pickle

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
# HYBRID PREDICTION
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
    # FINAL RESULT
    # ---------------------------------------------------

    return {

        "probability": lgb_prob,

        "lgb_prob": lgb_prob,

        "rf_prob": 0.0

    }