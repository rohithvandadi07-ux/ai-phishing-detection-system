import whois

from datetime import datetime
from urllib.parse import urlparse


# ---------------------------------------------------
# WHOIS DOMAIN INTELLIGENCE
# ---------------------------------------------------

def analyze_domain(url):

    indicators = []

    score = 0

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
        # DOMAIN AGE
        # ---------------------------------------------------

        if creation_date:

            age_days = (

                datetime.now() - creation_date

            ).days

            # Very new domain

            if age_days < 30:

                indicators.append(

                    f"Domain registered only {age_days} days ago"

                )

                score += 30

            elif age_days < 90:

                indicators.append(

                    "Recently registered domain"

                )

                score += 15

        else:

            indicators.append(

                "Unable to verify domain age"

            )

            score += 10

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

        # ---------------------------------------------------
        # REGISTRAR CHECK
        # ---------------------------------------------------

        if not data.registrar:

            indicators.append(

                "Missing registrar information"

            )

            score += 10

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

                break

        # ---------------------------------------------------
        # SUSPICIOUS TLD
        # ---------------------------------------------------

        suspicious_tlds = [

            ".xyz",
            ".top",
            ".buzz",
            ".click",
            ".shop",
            ".online",
            ".info"

        ]

        for tld in suspicious_tlds:

            if domain.endswith(tld):

                indicators.append(

                    f"Suspicious TLD detected ({tld})"

                )

                score += 12

                break

    except Exception:

        indicators.append(

            "WHOIS lookup failed"

        )

        score += 5

    return {

        "indicators": indicators,

        "score": score

    }