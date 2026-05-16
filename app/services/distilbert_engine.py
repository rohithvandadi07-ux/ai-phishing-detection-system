from transformers import pipeline

# ---------------------------------------------------
# LOAD DISTILBERT PIPELINE
# ---------------------------------------------------

classifier = pipeline(

    "text-classification",

    model=
    "distilbert-base-uncased-finetuned-sst-2-english"
)

# ---------------------------------------------------
# PHISHING KEYWORDS
# ---------------------------------------------------

PHISHING_WORDS = [

    "login",
    "verify",
    "bank",
    "paypal",
    "update",
    "secure",
    "account",
    "password",
    "signin",
    "confirm",
    "wallet",
    "crypto",
    "suspended",
    "unlock"
]

# ---------------------------------------------------
# SEMANTIC ANALYSIS
# ---------------------------------------------------

def semantic_phishing_check(url):

    try:

        text = url.lower()

        # ---------------------------------------------------
        # KEYWORD SCORE
        # ---------------------------------------------------

        keyword_hits = [

            word for word in PHISHING_WORDS
            if word in text
        ]

        keyword_score = (
            len(keyword_hits) * 0.08
        )

        # ---------------------------------------------------
        # DISTILBERT INFERENCE
        # ---------------------------------------------------

        result = classifier(text)[0]

        label =result["label"]

        confidence =float(result["score"])

        # ---------------------------------------------------
        # AI SCORE
        # ---------------------------------------------------

        ai_score = keyword_score

        reasons = []

        if keyword_hits:

            reasons.append(

                f"Semantic phishing keywords detected: {', '.join(keyword_hits)}"
            )

        # ---------------------------------------------------
        # SUSPICIOUS NLP
        # ---------------------------------------------------

        if confidence > 0.90:

            ai_score += 0.30

            reasons.append(

                "DistilBERT detected suspicious semantic structure"
            )

        # ---------------------------------------------------
        # FINAL SCORE
        # ---------------------------------------------------

        if ai_score > 1:

            ai_score = 1

        return {

            "score": round(ai_score, 4),

            "confidence": round(confidence, 4),

            "label": label,

            "reasons": reasons
        }

    except Exception as e:

        return {

            "score": 0,

            "confidence": 0,

            "label": "ERROR",

            "reasons": [

                str(e)
            ]
        }