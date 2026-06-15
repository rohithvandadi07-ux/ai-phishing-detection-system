from urllib.parse import urlparse


PHISHING_BRANDS = [
    "google",
    "paypal",
    "microsoft",
    "amazon",
    "apple",
    "facebook",
    "instagram",
    "github",
    "linkedin",
    "openai"
]


PHISHING_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "account",
    "signin",
    "update",
    "password",
    "confirm",
]


def build_threat_fingerprint(url):

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    brand = None

    for b in PHISHING_BRANDS:

        normalized = (
            domain
            .replace("0", "o")
            .replace("1", "l")
            .replace("3", "e")
            .replace("5", "s")
        )

        if b in normalized:

            brand = b.title()
            break

    keywords = []

    for kw in PHISHING_KEYWORDS:

        if kw in domain:

            keywords.append(kw)

    if "." in domain:

        tld = "." + domain.split(".")[-1]

    else:

        tld = ""

    return {

        "brand": brand,

        "keywords": keywords,

        "tld": tld,

        "domain": domain

    }


def classify_threat_family(url):

    fp = build_threat_fingerprint(url)

    family = "unknown"

    score = 0

    if fp["brand"]:

        family = f"{fp['brand'].lower()}-phishing"

        score += 50

    score += len(
        fp["keywords"]
    ) * 10

    suspicious_tlds = {

        ".xyz",
        ".top",
        ".click",
        ".zip",
        ".work"
    }

    if fp["tld"] in suspicious_tlds:

        score += 20

    score = min(
        score,
        100
    )

    return {

        "threat_family": family,

        "cluster_score": score,

        "fingerprint": fp

    }