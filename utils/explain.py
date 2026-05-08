from urllib.parse import urlparse


def explain_url(url):

    reasons = []

    lower_url = url.lower()

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    # -------------------------
    # Suspicious keywords
    # -------------------------

    suspicious_keywords = [
        "login",
        "secure",
        "verify",
        "update",
        "bank",
        "paypal",
        "signin",
        "account",
        "confirm",
        "password"
    ]

    for word in suspicious_keywords:

        if word in lower_url:
            reasons.append(f"Contains '{word}' keyword")

    # -------------------------
    # HTTP check
    # -------------------------

    if lower_url.startswith("http://"):
        reasons.append("Uses insecure HTTP")

    # -------------------------
    # Long URL
    # -------------------------

    if len(url) > 75:
        reasons.append("Very long URL")

    # -------------------------
    # Too many dots
    # -------------------------

    if domain.count(".") >= 3:
        reasons.append("Too many subdomains")

    # -------------------------
    # Suspicious TLDs
    # -------------------------

    suspicious_tlds = [
        ".xyz",
        ".top",
        ".tk",
        ".gq",
        ".ml",
        ".cf"
    ]

    for tld in suspicious_tlds:

        if domain.endswith(tld):
            reasons.append(f"Suspicious TLD: {tld}")

    # -------------------------
    # Typosquatting checks
    # -------------------------

    fake_brands = [
        "paypa1",
        "g00gle",
        "micr0soft",
        "faceb00k",
        "amaz0n"
    ]

    for brand in fake_brands:

        if brand in lower_url:
            reasons.append("Possible brand impersonation")

    return reasons