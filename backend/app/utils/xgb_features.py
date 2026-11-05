import re
import math
import ipaddress
from collections import Counter
from urllib.parse import urlparse, urlsplit, parse_qs

import tldextract


# Same configuration used in the Kaggle notebook
extractor = tldextract.TLDExtract(suffix_list_urls=None)


SUSPICIOUS_KEYWORDS = [
    "login", "signin", "verify", "verification",
    "account", "secure", "security", "update",
    "password", "banking", "confirm", "wallet",
    "payment", "authenticate", "credential",
    "recover", "unlock", "suspended", "validate"
]

URL_SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co",
    "goo.gl", "is.gd", "cutt.ly",
    "shorturl.at", "rebrand.ly"
]


# Kaggle Cell 7
def get_domain(url):
    try:
        parsed = urlparse(
            url if "://" in url else "//" + url
        )
        return parsed.hostname or ""
    except Exception:
        return ""


# Kaggle Cell 16
def get_registered_domain(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        hostname = urlsplit(url).hostname

        if not hostname:
            return None

        result = extractor(hostname)

        if result.domain and result.suffix:
            return result.domain + "." + result.suffix

        return hostname.lower()

    except Exception:
        return None


# Kaggle Cell 18
def extract_advanced_features(url):

    url = str(url).strip()
    malformed_url = 0

    try:
        parsed = urlparse(
            url if "://" in url else "http://" + url
        )

        hostname = parsed.hostname or ""
        path = parsed.path or ""
        query = parsed.query or ""

        try:
            port = parsed.port
            has_port = int(port is not None)
        except ValueError:
            has_port = 0
            malformed_url = 1

    except ValueError:
        malformed_url = 1
        hostname = ""
        path = url
        query = ""
        has_port = 0

    lower_url = url.lower()

    try:
        ipaddress.ip_address(hostname)
        has_ip = 1
    except ValueError:
        has_ip = 0

    digit_count = sum(c.isdigit() for c in url)
    special_count = sum(not c.isalnum() for c in url)

    frequency = Counter(url)

    entropy = -sum(
        (count / len(url)) * math.log2(count / len(url))
        for count in frequency.values()
    ) if url else 0

    return {
        "hostname_length": len(hostname),

        "domain_length": (
            len(hostname.split(".")[-2])
            if len(hostname.split(".")) >= 2
            else len(hostname)
        ),

        "path_length": len(path),
        "query_length": len(query),

        "query_parameters": len(parse_qs(query)),
        "subdirectory_count": path.count("/"),

        "hostname_dots": hostname.count("."),
        "hostname_hyphens": hostname.count("-"),

        "digit_ratio": digit_count / (len(url) + 1e-6),
        "special_char_ratio": special_count / (len(url) + 1e-6),

        "url_entropy": entropy,

        "has_ip_address": has_ip,
        "has_port": has_port,

        "has_punycode": int("xn--" in hostname),
        "has_encoded_chars": int("%" in url),
        "has_fragment": int("#" in url),
        "has_at_symbol": int("@" in url),

        "suspicious_keyword_count": sum(
            keyword in lower_url
            for keyword in SUSPICIOUS_KEYWORDS
        ),

        "is_shortened_url": int(
            any(shortener in hostname for shortener in URL_SHORTENERS)
        ),

        "has_malformed_url": malformed_url
    }


# Exact feature order from model_metadata.json
FEATURE_NAMES = [
    "url_length",
    "num_dots",
    "num_hyphens",
    "num_digits",
    "num_special_chars",
    "num_subdomains",
    "has_https",
    "has_ip",
    "has_at_symbol",
    "hostname_length",
    "domain_length",
    "path_length",
    "query_length",
    "query_parameters",
    "subdirectory_count",
    "hostname_hyphens",
    "digit_ratio",
    "special_char_ratio",
    "url_entropy",
    "has_port",
    "has_punycode",
    "has_encoded_chars",
    "has_fragment",
    "suspicious_keyword_count",
    "is_shortened_url",
    "has_malformed_url",
    "missing_registered_domain"
]


def extract_xgb_features(url):
    """Extract the exact 27 features expected by the trained XGBoost model."""

    url = str(url).strip()

    # Basic features: Kaggle Cell 7
    domain = get_domain(url)

    basic_features = {
        "url_length": len(url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_digits": len(re.findall(r"\d", url)),
        "num_special_chars": sum(not c.isalnum() for c in url),
        "num_subdomains": max(0, len(domain.split(".")) - 2),
        "has_https": int(url.lower().startswith("https://")),
        "has_ip": int(bool(
            re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", domain)
        )),
        "has_at_symbol": int("@" in url)
    }

    # Advanced features: Kaggle Cell 18
    advanced_features = extract_advanced_features(url)

    # Registered-domain feature: Kaggle Cells 16 and 22
    missing_registered_domain = int(
        get_registered_domain(url) is None
    )

    # Combine and preserve exact model feature order
    all_features = {
        **basic_features,
        **advanced_features,
        "missing_registered_domain": missing_registered_domain
    }

    return [all_features[name] for name in FEATURE_NAMES]
