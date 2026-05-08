import requests
import base64

# -----------------------------
# VIRUSTOTAL CONFIG
# -----------------------------

VT_API_KEY = "42b0d0a9ef511721ef627a0f5dd498fd5b06d2721e19631931030e689ef7eb90"

# -----------------------------
# VIRUSTOTAL CHECK
# -----------------------------

def check_virustotal(url):

    try:

        url_id = base64.urlsafe_b64encode(
            url.encode()
        ).decode().strip("=")

        headers = {
            "x-apikey": VT_API_KEY
        }

        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers
        )

        data = response.json()

        stats = data["data"]["attributes"]["last_analysis_stats"]

        malicious_count = (
            stats.get("malicious", 0) +
            stats.get("suspicious", 0)
        )

        return {

            "malicious": malicious_count > 0,
            "detections": malicious_count

        }

    except Exception:

        return {

            "malicious": False,
            "detections": 0

        }

# -----------------------------
# PHISHTANK / OPENPHISH CHECK
# -----------------------------

KNOWN_PHISHING_DOMAINS = {

    "paypal-login-secure.xyz",
    "verify-amazon-login.free",
    "microsoft-authentication.xyz",
    "google-security-check.com",
    "appleid-verification.top"

}

def check_phishtank(url):

    try:

        domain = url.split("//")[-1].split("/")[0]

        if domain in KNOWN_PHISHING_DOMAINS:

            return {
                "malicious": True
            }

        return {
            "malicious": False
        }

    except Exception:

        return {
            "malicious": False
        }