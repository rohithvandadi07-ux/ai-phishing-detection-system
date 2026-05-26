import os
import base64
import requests

from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENV
# ---------------------------------------------------

load_dotenv()

VT_API_KEY = os.getenv(
    "VIRUSTOTAL_API_KEY"
)

# ---------------------------------------------------
# HEADERS
# ---------------------------------------------------

HEADERS = {

    "x-apikey": VT_API_KEY
}

# ---------------------------------------------------
# URL ENCODER
# ---------------------------------------------------

def url_to_id(url):

    encoded = base64.urlsafe_b64encode(

        url.encode()

    ).decode().strip("=")

    return encoded

# ---------------------------------------------------
# DEFAULT RESPONSE
# ---------------------------------------------------

def default_response():

    return {

        "found": False,

        "status": "unknown",

        "confidence": 0.0,

        "malicious": 0,

        "suspicious": 0,

        "harmless": 0,

        "undetected": 0,

        "total_engines": 0,

        "message": "No VirusTotal data"
    }

# ---------------------------------------------------
# VIRUSTOTAL LOOKUP
# ---------------------------------------------------

def get_virustotal_report(url):

    try:

        if not VT_API_KEY:

            return {

                **default_response(),

                "status": "error",

                "message": "VirusTotal API key missing"
            }

        # ---------------------------------------------------
        # ENCODE URL
        # ---------------------------------------------------

        url_id = url_to_id(url)

        vt_url = (

            f"https://www.virustotal.com/api/v3/urls/{url_id}"
        )

        # ---------------------------------------------------
        # FETCH REPORT
        # ---------------------------------------------------

        response = requests.get(

            vt_url,

            headers=HEADERS,

            timeout=15
        )

        # ---------------------------------------------------
        # REPORT EXISTS
        # ---------------------------------------------------

        if response.status_code == 200:

            data = response.json()

            stats = data["data"]["attributes"][
                "last_analysis_stats"
            ]

            malicious = stats.get(
                "malicious",
                0
            )

            suspicious = stats.get(
                "suspicious",
                0
            )

            harmless = stats.get(
                "harmless",
                0
            )

            undetected = stats.get(
                "undetected",
                0
            )

            total = sum(stats.values())

            detection_ratio = (

                malicious + suspicious

            ) / max(total, 1)

            # ---------------------------------------------------
            # STATUS
            # ---------------------------------------------------

            if malicious >= 3:

                status = "malicious"

            elif suspicious >= 2:

                status = "suspicious"

            else:

                status = "safe"

            return {

                "found": True,

                "status": status,

                "confidence": round(
                    detection_ratio,
                    4
                ),

                "malicious": malicious,

                "suspicious": suspicious,

                "harmless": harmless,

                "undetected": undetected,

                "total_engines": total,

                "message": "VirusTotal report fetched"
            }

        # ---------------------------------------------------
        # REPORT NOT FOUND
        # ---------------------------------------------------

        elif response.status_code == 404:

            submit_response = requests.post(

                "https://www.virustotal.com/api/v3/urls",

                headers=HEADERS,

                data={
                    "url": url
                },

                timeout=15
            )

            if submit_response.status_code in [
                200,
                202
            ]:

                return {

                    **default_response(),

                    "status": "submitted",

                    "message": "URL submitted to VirusTotal"
                }

        # ---------------------------------------------------
        # RATE LIMIT
        # ---------------------------------------------------

        elif response.status_code == 429:

            return {

                **default_response(),

                "status": "rate_limited",

                "message": "VirusTotal rate limit exceeded"
            }

        # ---------------------------------------------------
        # INVALID API KEY
        # ---------------------------------------------------

        elif response.status_code == 401:

            return {

                **default_response(),

                "status": "error",

                "message": "Invalid VirusTotal API key"
            }

        # ---------------------------------------------------
        # OTHER ERRORS
        # ---------------------------------------------------

        return {

            **default_response(),

            "status": "error",

            "message": f"VirusTotal Error {response.status_code}"
        }

    except Exception as e:

        return {

            **default_response(),

            "status": "error",

            "message": str(e)
        }