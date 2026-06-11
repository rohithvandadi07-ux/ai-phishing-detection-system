# app/services/reputation_engine.py

import math
import re

from urllib.parse import urlparse


# ---------------------------------------------------
# TRUSTED BRANDS
# ---------------------------------------------------

TRUSTED_BRANDS = [

    "google",
    "microsoft",
    "paypal",
    "amazon",
    "apple",
    "github",
    "facebook",
    "instagram",
    "netflix",
    "openai",
    "linkedin",
    "dropbox",
    "x.com",
    "twitter"
]

# ---------------------------------------------------
# TYPOSQUATTING VARIANTS
# ---------------------------------------------------

TYPOSQUAT_VARIANTS = {

    "google": [
        "g00gle",
        "goog1e"
    ],

    "facebook": [
        "faceb00k",
        "facebo0k"
    ],

    "amazon": [
        "amaz0n"
    ],

    "paypal": [
        "paypa1",
        "paypai"
    ],

    "microsoft": [
        "micr0soft"
    ]
}

# ---------------------------------------------------
# SUSPICIOUS TLDS
# ---------------------------------------------------

SUSPICIOUS_TLDS = [

    ".xyz",
    ".top",
    ".buzz",
    ".click",
    ".shop",
    ".online",
    ".info",
    ".ru",
    ".tk",
    ".cf",
    ".gq",
    ".ml",
    ".ga"
]

# ---------------------------------------------------
# PHISHING KEYWORDS
# ---------------------------------------------------

PHISHING_KEYWORDS = [

    "login",
    "signin",
    "verify",
    "secure",
    "account",
    "wallet",
    "bank",
    "update",
    "authenticate",
    "billing",
    "otp",
    "confirm",
    "password",
    "crypto"
]

# ---------------------------------------------------
# DOMAIN ENTROPY
# ---------------------------------------------------

def calculate_entropy(text):

    if not text:

        return 0

    probabilities = [

        float(text.count(char)) / len(text)

        for char in dict.fromkeys(list(text))
    ]

    entropy = -sum(

        p * math.log(p) / math.log(2.0)

        for p in probabilities
    )

    return entropy

# ---------------------------------------------------
# MAIN REPUTATION ANALYZER
# ---------------------------------------------------

def analyze_reputation(url):

    score = 0

    indicators = []

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    full_url = url.lower()

    # ---------------------------------------------------
    # REMOVE WWW
    # ---------------------------------------------------

    if domain.startswith("www."):

        domain = domain[4:]

    # ---------------------------------------------------
    # SUSPICIOUS TLD
    # ---------------------------------------------------

    for tld in SUSPICIOUS_TLDS:

        if domain.endswith(tld):

            score += 20

            indicators.append(

                f"Suspicious TLD detected ({tld})"
            )

            break

    # ---------------------------------------------------
    # PHISHING KEYWORDS
    # ---------------------------------------------------

    keyword_hits = 0

    for keyword in PHISHING_KEYWORDS:

        if keyword in full_url:

            keyword_hits += 1

    if keyword_hits >= 3:

        score += 30

        indicators.append(

            "Multiple phishing-related keywords detected"
        )

    elif keyword_hits == 2:

        score += 18

        indicators.append(

            "Suspicious authentication keywords detected"
        )

    elif keyword_hits == 1:

        score += 8

    # ---------------------------------------------------
    # BRAND IMPERSONATION
    # ---------------------------------------------------

    for brand in TRUSTED_BRANDS:

        if brand in domain:

            trusted_patterns = [

                f"{brand}.com",
                f".{brand}.com"

            ]

            is_legit = any(

                domain == p.lstrip(".")
                or domain.endswith(p)

                for p in trusted_patterns
            )

            if not is_legit:

                score += 35

                indicators.append(

                    f"Potential {brand} impersonation detected"
                )

                break

    # ---------------------------------------------------
    # TYPOSQUATTING DETECTION
    # ---------------------------------------------------

    for brand, variants in TYPOSQUAT_VARIANTS.items():

        for variant in variants:

            if variant in domain:

                score += 40

                indicators.append(
                    f"Possible {brand} typosquatting domain"
                )

                break

    # ---------------------------------------------------
    # TYPOSQUATTING DETECTION
    # ---------------------------------------------------

    for brand, variants in TYPOSQUAT_VARIANTS.items():

        for variant in variants:

            if variant in domain:

                score += 40

                indicators.append(

                    f"Possible {brand} typosquatting domain"
                )

                break

    # ---------------------------------------------------
    # TYPOSQUATTING DETECTION
    # ---------------------------------------------------

    for brand, variants in TYPOSQUAT_VARIANTS.items():

        for variant in variants:

            if variant in domain:

                score += 40

                indicators.append(

                    f"Possible {brand} typosquatting domain"
                )

                break

    # ---------------------------------------------------
    # TOO MANY SUBDOMAINS
    # ---------------------------------------------------

    subdomain_count = domain.count(".")

    if subdomain_count >= 3:

        score += 15

        indicators.append(

            "Excessive subdomain structure detected"
        )

    # ---------------------------------------------------
    # RANDOM LOOKING DOMAIN
    # ---------------------------------------------------

    entropy = calculate_entropy(domain)

    if entropy >= 4.0:

        score += 20

        indicators.append(

            "Randomized domain pattern detected"
        )

    # ---------------------------------------------------
    # URL LENGTH
    # ---------------------------------------------------

    if len(full_url) >= 120:

        score += 15

        indicators.append(

            "Excessively long URL detected"
        )

    # ---------------------------------------------------
    # SPECIAL CHARACTERS
    # ---------------------------------------------------

    special_chars = len(

        re.findall(
            r"[@_\-%=]",
            full_url
        )
    )

    if special_chars >= 4:

        score += 10

        indicators.append(

            "Suspicious URL symbol usage detected"
        )

    # ---------------------------------------------------
    # HTTPS CHECK
    # ---------------------------------------------------

    if not full_url.startswith("https://"):

        score += 12

        indicators.append(

            "Website does not use HTTPS"
        )

    # ---------------------------------------------------
    # CLAMP SCORE
    # ---------------------------------------------------

    score = min(score, 100)

    # ---------------------------------------------------
    # TRUST LEVEL
    # ---------------------------------------------------

    if score >= 80:

        level = "CRITICAL"

    elif score >= 60:

        level = "HIGH"

    elif score >= 40:

        level = "MODERATE"

    elif score >= 20:

        level = "LOW"

    else:

        level = "SAFE"

    # ---------------------------------------------------
    # RETURN
    # ---------------------------------------------------

    return {

        "reputation_score": score,

        "reputation_level": level,

        "indicators": indicators
    }