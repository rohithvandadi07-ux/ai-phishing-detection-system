from difflib import SequenceMatcher
from urllib.parse import urlparse

TRUSTED_BRANDS = {

    "google.com",
    "microsoft.com",
    "paypal.com",
    "amazon.com",
    "apple.com",
    "facebook.com",
    "instagram.com",
    "netflix.com",
    "github.com",
    "linkedin.com",
    "openai.com"

}

BRANDS = [
    "google",
    "microsoft",
    "paypal",
    "amazon",
    "apple",
    "facebook",
    "instagram",
    "netflix",
    "github",
    "linkedin",
    "openai",
    "dropbox",
    "twitter",
    "x",
    "telegram",
    "whatsapp",
    "adobe",
    "spotify",
]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


def extract_domain(url: str) -> str:

    try:

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:

        return url.lower()

def detect_brand_impersonation(url):

    domain = extract_domain(url)

    if domain in TRUSTED_BRANDS:

        return {

            "detected": False,

            "brand": None,

            "confidence": 0.0,

            "reason": None

        }

    normalized = (

        domain
        .replace("0", "o")
        .replace("1", "l")
        .replace("3", "e")
        .replace("5", "s")
        .replace("@", "a")

    )

    tokens = []

    for part in normalized.replace(".", "-").split("-"):

        if part:

            tokens.append(part)

    best_brand = None
    best_score = 0.0

    for brand in BRANDS:

        if brand in normalized:

            return {

                "detected": True,

                "brand": brand.title(),

                "confidence": 1.0,

                "reason": f"Brand keyword '{brand}' found"

            }

        for token in tokens:

            score = similarity(

                token,
                brand

            )

            if score > best_score:

                best_score = score

                best_brand = brand

    if best_score >= 0.75:

        return {

            "detected": True,

            "brand": best_brand.title(),

            "confidence": round(
                best_score,
                3
            ),

            "reason": "Possible brand impersonation"

        }

    return {

        "detected": False,

        "brand": None,

        "confidence": 0.0,

        "reason": None

    }