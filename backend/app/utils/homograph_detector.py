from urllib.parse import urlparse

# -----------------------------------
# HOMOGRAPH CHARACTERS
# -----------------------------------

HOMOGRAPH_MAP = {

    "а": "a",  # Cyrillic
    "е": "e",
    "о": "o",
    "р": "p",
    "с": "c",
    "у": "y",
    "х": "x",

    "ο": "o",  # Greek
    "ρ": "p",
    "ν": "v",
    "ι": "i",
    "κ": "k"
}

# -----------------------------------
# DETECTOR
# -----------------------------------

def detect_homograph_attack(url):

    indicators = []

    score = 0

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    suspicious_chars = []

    for char in domain:

        if char in HOMOGRAPH_MAP:

            suspicious_chars.append(char)

    if suspicious_chars:

        indicators.append(
            "Unicode homograph characters detected"
        )

        score += 50

    return {

        "score": score,
        "indicators": indicators,
        "characters": suspicious_chars
    }