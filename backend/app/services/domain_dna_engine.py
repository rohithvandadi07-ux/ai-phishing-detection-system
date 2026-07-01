import math
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "update",
    "account",
    "signin",
    "confirm",
    "password",
]


SUSPICIOUS_TLDS = [
    ".xyz",
    ".top",
    ".click",
    ".zip",
    ".review",
    ".country",
    ".work",
]

def calculate_entropy(text):

    if not text:
        return 0

    entropy = 0

    for char in set(text):
        p = text.count(char) / len(text)
        entropy -= p * math.log2(p)

    return round(entropy, 3)


def analyze_domain_dna(url):

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    entropy = calculate_entropy(domain)

    digit_ratio = (
        sum(c.isdigit() for c in domain)
        / max(len(domain), 1)
    )

    hyphen_ratio = (
        domain.count("-")
        / max(len(domain), 1)
    )

    subdomain_depth = max(
        len(domain.split(".")) - 2,
        0
    )

    keyword_hits = sum(
        keyword in domain
        for keyword in SUSPICIOUS_KEYWORDS
    )

    keyword_density = (
        keyword_hits
        / len(SUSPICIOUS_KEYWORDS)
    )

    tld_risk = 1 if any(
        domain.endswith(tld)
        for tld in SUSPICIOUS_TLDS
    ) else 0

    dna_score = 0

    dna_score += entropy * 5
    dna_score += digit_ratio * 100
    dna_score += hyphen_ratio * 100
    dna_score += keyword_density * 100
    dna_score += subdomain_depth * 10
    dna_score += tld_risk * 20

    dna_score = min(
        round(dna_score),
        100
    )

    return {

        "dna_score": dna_score,

        "entropy": entropy,

        "digit_ratio": round(
            digit_ratio,
            3
        ),

        "hyphen_ratio": round(
            hyphen_ratio,
            3
        ),

        "subdomain_depth": subdomain_depth,

        "keyword_density": round(
            keyword_density,
            3
        ),

        "tld_risk": tld_risk

    }