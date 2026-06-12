import requests

from urllib.parse import urlparse

# ---------------------------------------------------
# URL SHORTENERS
# ---------------------------------------------------

SHORTENERS = {

    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "rebrand.ly",
    "cutt.ly",
    "shorturl.at"

}


# ---------------------------------------------------
# REDIRECT INTELLIGENCE
# ---------------------------------------------------

def analyze_redirects(url):

    redirects = []

    indicators = []

    score = 0

    try:

        response = requests.get(

            url,

            allow_redirects=True,

            timeout=10
        )

        history = response.history

        # -------------------------------------------
        # REDIRECT CHAIN
        # -------------------------------------------

        for hop in history:

            redirects.append(
                hop.url
            )

        redirects.append(
            response.url
        )

        # -------------------------------------------
        # SCORING
        # -------------------------------------------

        redirect_count = len(history)

        # -------------------------------------------
        # URL SHORTENER DETECTION
        # -------------------------------------------

        original_domain = urlparse(
            url
        ).netloc.lower()

        final_domain = urlparse(
            response.url
        ).netloc.lower()

        if original_domain in SHORTENERS:

            indicators.append(
                "URL shortener detected"
            )

            score += 5

        # -------------------------------------------
        # DOMAIN SWITCH DETECTION
        # -------------------------------------------

        if original_domain != final_domain:

            indicators.append(
                "Redirected to different domain"
            )

            score += 5

        if redirect_count >= 3:

            score += 25

        elif redirect_count >= 2:

            score += 15

        elif redirect_count >= 1:

            score += 5

        return {

            "score": score,

            "redirect_count": redirect_count,

            "final_url": response.url,

            "chain": redirects,

            "indicators": indicators

        }

    except Exception:

        return {

            "score": 0,

            "redirect_count": 0,

            "final_url": url,

            "chain": [],

            "indicators": [

                "Redirect analysis failed"
            ]

        }