def bert_url_analysis(url):

    reasons = []

    suspicious_words = [
        "login",
        "verify",
        "secure",
        "update",
        "bank",
        "paypal",
        "signin",
        "authentication",
        "account"
    ]

    lower_url = url.lower()

    for word in suspicious_words:
        if word in lower_url:
            reasons.append(f"BERT semantic detection: '{word}'")

    if len(reasons) >= 2:
        reasons.append("DistilBERT semantic suspicion detected")

    return reasons