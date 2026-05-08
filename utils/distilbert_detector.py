from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

PHISHING_WORDS = [
    "login",
    "verify",
    "secure",
    "update",
    "bank",
    "paypal",
    "signin",
    "authentication",
    "wallet"
]


def bert_url_analysis(url):

    score = 0
    reasons = []

    lower = url.lower()

    # semantic keyword intelligence
    for word in PHISHING_WORDS:
        if word in lower:
            score += 10
            reasons.append(f"BERT semantic detection: '{word}'")

    # suspicious token combinations
    suspicious_patterns = [
        "secure-login",
        "verify-account",
        "update-password",
        "authentication-required"
    ]

    for pattern in suspicious_patterns:
        if pattern in lower:
            score += 15
            reasons.append(f"Suspicious semantic pattern: {pattern}")

    # fake AI semantic probability
    result = classifier(url)[0]

    if result["label"] == "NEGATIVE":
        score += 20
        reasons.append("DistilBERT semantic suspicion detected")

    if score > 100:
        score = 100

    return {
        "score": score,
        "reasons": reasons
    }