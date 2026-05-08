from urllib.parse import urlparse
import difflib

# Trusted brands
BRANDS = [
    "google",
    "paypal",
    "amazon",
    "facebook",
    "microsoft",
    "apple",
    "netflix",
    "linkedin",
    "instagram",
    "github"
]

# Suspicious TLDs commonly used in phishing
SUSPICIOUS_TLDS = [
    ".xyz", ".top", ".tk", ".gq", ".ml",
    ".click", ".buzz", ".shop", ".country"
]


def is_typosquatting(domain, brand):
    similarity = difflib.SequenceMatcher(None, domain, brand).ratio()
    return similarity > 0.75 and domain != brand


def explain_url(url):
    reasons = []

    parsed = urlparse(url)
    hostname = parsed.netloc.lower()

    # remove www
    if hostname.startswith("www."):
        hostname = hostname[4:]

    # remove TLD for comparison
    domain_name = hostname.split(".")[0]

    # -----------------------------------
    # Typosquatting / brand impersonation
    # -----------------------------------
    for brand in BRANDS:

        if brand in hostname and hostname != f"{brand}.com":
            reasons.append(f"Possible fake '{brand}' domain")

        elif is_typosquatting(domain_name, brand):
            reasons.append(f"Typosquatting detected for '{brand}'")

    # -----------------------------------
    # Suspicious TLD
    # -----------------------------------
    for tld in SUSPICIOUS_TLDS:
        if hostname.endswith(tld):
            reasons.append(f"Suspicious TLD detected ({tld})")

    # -----------------------------------
    # Existing checks
    # -----------------------------------
    if "login" in url.lower():
        reasons.append("Contains 'login' keyword")

    if "verify" in url.lower():
        reasons.append("Contains 'verify' keyword")

    if "secure" in url.lower():
        reasons.append("Contains 'secure' keyword")

    if url.startswith("http://"):
        reasons.append("Uses insecure HTTP")

    if url.count("-") >= 3:
        reasons.append("Too many hyphens in URL")

    if url.count(".") >= 5:
        reasons.append("Too many subdomains")

    if not reasons:
        reasons.append("No strong phishing indicators detected")

    return reasons