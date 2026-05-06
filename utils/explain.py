def explain_url(url):
    reasons = []

    if "login" in url.lower():
        reasons.append("Contains 'login' keyword")

    if "http://" in url:
        reasons.append("Uses insecure HTTP")

    if len(url) > 75:
        reasons.append("URL is unusually long")

    if any(char.isdigit() for char in url):
        reasons.append("Contains numeric patterns")

    # 🔥 ADD THIS (IMPORTANT)
    if not reasons:
        reasons.append("Model detected statistical anomaly")

    return reasons