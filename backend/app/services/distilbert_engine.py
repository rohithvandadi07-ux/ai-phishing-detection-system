# ---------------------------------------------------
# PHISHING KEYWORDS ENGINE
# ---------------------------------------------------

PHISHING_WORDS = [

    "login",
    "verify",
    "bank",
    "paypal",
    "update",
    "secure",
    "account",
    "password",
    "signin",
    "confirm",
    "wallet",
    "crypto",
    "suspended",
    "unlock",
    "billing",
    "authenticate",
    "recovery",
    "otp"

]

# ---------------------------------------------------
# TRUSTED DOMAINS
# ---------------------------------------------------

SAFE_DOMAINS = [

    "google.com",
    "github.com",
    "openai.com",
    "microsoft.com",
    "apple.com",
    "amazon.com",
    "youtube.com",
    "linkedin.com",

    "facebook.com",
    "instagram.com",
    "x.com",
    "twitter.com",

    "stackoverflow.com",
    "reddit.com",

    "netflix.com",
    "adobe.com",

    "oracle.com",
    "ibm.com"

]

# ---------------------------------------------------
# SEMANTIC ANALYSIS
# ---------------------------------------------------

def semantic_phishing_check(url):

    try:

        text = url.lower()

        # ---------------------------------------------------
        # SAFE DOMAIN OVERRIDE
        # ---------------------------------------------------

        if any(

            domain in text

            for domain in SAFE_DOMAINS

        ):

            return {

                "score": 0.0,

                "confidence": 0.0,

                "label": "SAFE_DOMAIN",

                "reasons": []

            }

        # ---------------------------------------------------
        # KEYWORD MATCHING
        # ---------------------------------------------------

        keyword_hits = [

            word

            for word in PHISHING_WORDS

            if word in text

        ]

        # ---------------------------------------------------
        # SCORE
        # ---------------------------------------------------

        ai_score = (

            len(keyword_hits) * 0.08

        )

        reasons = []

        # ---------------------------------------------------
        # REASONS
        # ---------------------------------------------------

        if keyword_hits:

            reasons.append(

                "Semantic phishing keywords detected: "

                + ", ".join(keyword_hits)

            )

        if len(keyword_hits) >= 2:

            ai_score += 0.25

            reasons.append(

                "Multiple phishing keywords detected"

            )

        if len(keyword_hits) >= 4:

            ai_score += 0.20

            reasons.append(

                "High concentration of phishing language"

            )

        # ---------------------------------------------------
        # URL STRUCTURE SIGNALS
        # ---------------------------------------------------

        if "@" in text:

            ai_score += 0.15

            reasons.append(

                "@ symbol obfuscation detected"

            )

        if text.count("-") >= 3:

            ai_score += 0.10

            reasons.append(

                "Multiple hyphens detected"

            )

        if text.count(".") >= 4:

            ai_score += 0.10

            reasons.append(

                "Too many subdomains detected"

            )

        # ---------------------------------------------------
        # CLAMP
        # ---------------------------------------------------

        ai_score = min(

            ai_score,

            1.0

        )

        return {

            "score": round(

                ai_score,

                4

            ),

            "confidence": round(

                ai_score,

                4

            ),

            "label": "URL_ANALYZER",

            "reasons": reasons

        }

    except Exception as e:

        return {

            "score": 0.0,

            "confidence": 0.0,

            "label": "ERROR",

            "reasons": [

                str(e)

            ]

        }