import whois

from datetime import datetime
from urllib.parse import urlparse


# ---------------------------------------------------
# TRUSTED REGISTRARS
# ---------------------------------------------------

TRUSTED_REGISTRARS = [

    "godaddy",
    "namecheap",
    "google",
    "cloudflare",
    "amazon",
    "name.com"
]

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
    ".gq",
    ".ml",
    ".cf",
    ".ga"
]

# ---------------------------------------------------
# ANALYZE DOMAIN
# ---------------------------------------------------

def analyze_domain(url):

    indicators = []

    score = 0

    trust_score = 100

    registrar_name = "Unknown"

    domain_age_days = None

    try:

        # ---------------------------------------------------
        # EXTRACT DOMAIN
        # ---------------------------------------------------

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        if domain.startswith("www."):

            domain = domain[4:]

        # ---------------------------------------------------
        # WHOIS LOOKUP
        # ---------------------------------------------------

        data = whois.whois(domain)

        # ---------------------------------------------------
        # CREATION DATE
        # ---------------------------------------------------

        creation_date = data.creation_date

        if isinstance(creation_date, list):

            creation_date = creation_date[0]

        # ---------------------------------------------------
        # EXPIRATION DATE
        # ---------------------------------------------------

        expiration_date = data.expiration_date

        if isinstance(expiration_date, list):

            expiration_date = expiration_date[0]

        # ---------------------------------------------------
        # REGISTRAR
        # ---------------------------------------------------

        if data.registrar:

            registrar_name = str(
                data.registrar
            )

        # ---------------------------------------------------
        # DOMAIN AGE
        # ---------------------------------------------------

        if creation_date:

            domain_age_days = (

                datetime.now() - creation_date

            ).days

            # -----------------------------------------------
            # VERY NEW DOMAIN
            # -----------------------------------------------

            if domain_age_days < 7:

                indicators.append(
                    "Extremely new domain detected"
                )

                score += 40

                trust_score -= 45

            elif domain_age_days < 30:

                indicators.append(
                    f"Domain registered only {domain_age_days} days ago"
                )

                score += 30

                trust_score -= 35

            elif domain_age_days < 90:

                indicators.append(
                    "Recently registered domain"
                )

                score += 15

                trust_score -= 20

            elif domain_age_days > 1000:

                indicators.append(
                    "Old established domain"
                )

                trust_score += 10

        else:

            indicators.append(
                "Unable to verify domain age"
            )

            score += 10

            trust_score -= 10

        # ---------------------------------------------------
        # EXPIRATION CHECK
        # ---------------------------------------------------

        if expiration_date:

            remaining_days = (

                expiration_date - datetime.now()

            ).days

            if remaining_days < 30:

                indicators.append(
                    "Domain expires very soon"
                )

                score += 15

                trust_score -= 15

        # ---------------------------------------------------
        # REGISTRAR REPUTATION
        # ---------------------------------------------------

        registrar_lower = registrar_name.lower()

        trusted = any(

            trusted_name in registrar_lower

            for trusted_name in TRUSTED_REGISTRARS
        )

        if trusted:

            indicators.append(
                "Trusted registrar detected"
            )

            trust_score += 5

        else:

            # informational only

            indicators.append(
                "Registrar not in trusted list"
            )

        # ---------------------------------------------------
        # WHOIS PRIVACY
        # ---------------------------------------------------

        raw_text = str(data).lower()

        privacy_keywords = [

            "redacted",
            "privacy",
            "hidden",
            "protected"
        ]

        for keyword in privacy_keywords:

            if keyword in raw_text:

                indicators.append(
                    "WHOIS identity protection detected"
                )

                score += 8

                trust_score -= 8

                break

        # ---------------------------------------------------
        # SUSPICIOUS TLD
        # ---------------------------------------------------

        for tld in SUSPICIOUS_TLDS:

            if domain.endswith(tld):

                indicators.append(
                    f"Suspicious TLD detected ({tld})"
                )

                score += 12

                trust_score -= 15

                break

        # ---------------------------------------------------
        # FINAL CLAMP
        # ---------------------------------------------------

        trust_score = max(

            0,

            min(
                trust_score,
                100
            )
        )

    except Exception:

        indicators.append(
            "WHOIS lookup failed"
        )

        score += 5

        trust_score -= 5

    # ---------------------------------------------------
    # FINAL RESPONSE
    # ---------------------------------------------------

    return {

        "indicators": indicators,

        "score": score,

        "trust_score": trust_score,

        "registrar": registrar_name,

        "domain_age_days": domain_age_days
    }