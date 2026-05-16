import ssl
import socket
import whois
from urllib.parse import urlparse
from datetime import datetime


# ---------------------------------------------------
# Suspicious registrars
# ---------------------------------------------------

SUSPICIOUS_REGISTRARS = {

    "namecheap",
    "sav",
    "publicdomainregistry",
    "hostinger"

}


# ---------------------------------------------------
# DOMAIN INTELLIGENCE ENGINE
# ---------------------------------------------------

def analyze_domain_intelligence(url):

    indicators = []
    score = 0

    try:

        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        # ---------------------------------------------------
        # HTTPS CHECK
        # ---------------------------------------------------

        if not url.startswith("https://"):

            indicators.append(
                "Website does not use HTTPS"
            )

            score += 20

        # ---------------------------------------------------
        # SSL CERTIFICATE CHECK
        # ---------------------------------------------------

        try:

            context = ssl.create_default_context()

            with socket.create_connection((domain, 443), timeout=3) as sock:

                with context.wrap_socket(
                    sock,
                    server_hostname=domain
                ) as ssock:

                    cert = ssock.getpeercert()

                    if not cert:

                        indicators.append(
                            "Invalid SSL certificate"
                        )

                        score += 20

        except Exception:

            indicators.append(
                "SSL certificate validation failed"
            )

            score += 20

        # ---------------------------------------------------
        # WHOIS LOOKUP
        # ---------------------------------------------------

        try:

            w = whois.whois(domain)

            creation_date = w.creation_date

            # Some WHOIS providers return list
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            if creation_date:

                domain_age = (
                    datetime.now() - creation_date
                ).days

                # Recently created domains
                if domain_age < 30:

                    indicators.append(
                        "Very new domain"
                    )

                    score += 35

                elif domain_age < 180:

                    indicators.append(
                        "Recently registered domain"
                    )

                    score += 20

            # Registrar analysis
            registrar = str(w.registrar).lower()

            for bad_registrar in SUSPICIOUS_REGISTRARS:

                if bad_registrar in registrar:

                    indicators.append(
                        f"Suspicious registrar ({bad_registrar})"
                    )

                    score += 15

                    break

        except Exception:

            indicators.append(
                "WHOIS information unavailable"
            )

            score += 10

        return {

            "score": score,
            "indicators": indicators

        }

    except Exception:

        return {

            "score": 0,
            "indicators": []

        }