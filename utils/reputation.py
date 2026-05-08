from urllib.parse import urlparse
import re


# -----------------------------
# Suspicious TLDs
# -----------------------------

SUSPICIOUS_TLDS = {

    ".xyz",
    ".top",
    ".gq",
    ".tk",
    ".ml",
    ".cf",
    ".buzz",
    ".click",
    ".work",
    ".support",
    ".country"

}


# -----------------------------
# Popular brands
# -----------------------------

POPULAR_BRANDS = {

    "google",
    "paypal",
    "amazon",
    "microsoft",
    "apple",
    "facebook",
    "instagram",
    "linkedin",
    "netflix",
    "bank"

}


# -----------------------------
# Reputation Analysis Engine
# -----------------------------

def analyze_url_reputation(url):

    indicators = []
    reputation_score = 0

    try:

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Remove www
        if domain.startswith("www."):
            domain = domain[4:]

        # -----------------------------
        # Suspicious TLD detection
        # -----------------------------

        for tld in SUSPICIOUS_TLDS:

            if domain.endswith(tld):

                indicators.append(
                    f"Suspicious TLD detected ({tld})"
                )

                reputation_score += 25

        # -----------------------------
        # Excessive subdomains
        # -----------------------------

        if domain.count(".") >= 3:

            indicators.append(
                "Too many subdomains"
            )

            reputation_score += 15

        # -----------------------------
        # Brand impersonation
        # -----------------------------

        for brand in POPULAR_BRANDS:

            if brand in domain:

                # Example:
                # google-login-secure.xyz

                if domain != f"{brand}.com":

                    indicators.append(
                        f"Possible {brand} impersonation"
                    )

                    reputation_score += 30

        # -----------------------------
        # Numeric-heavy domains
        # -----------------------------

        numbers = re.findall(r"\d", domain)

        if len(numbers) >= 5:

            indicators.append(
                "Numeric-heavy domain"
            )

            reputation_score += 15

        # -----------------------------
        # Hyphen abuse
        # -----------------------------

        if domain.count("-") >= 3:

            indicators.append(
                "Excessive hyphen usage"
            )

            reputation_score += 20

        # -----------------------------
        # Long domain detection
        # -----------------------------

        if len(domain) > 35:

            indicators.append(
                "Unusually long domain"
            )

            reputation_score += 20

        return {

            "score": reputation_score,
            "indicators": indicators

        }

    except Exception:

        return {

            "score": 0,
            "indicators": []

        }