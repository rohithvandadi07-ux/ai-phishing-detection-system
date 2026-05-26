import os
import time
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

headers = {

    "x-apikey": VT_API_KEY
}

# ---------------------------------------------------
# URL ENCODER
# ---------------------------------------------------

def url_to_id(url):

    url_bytes = url.encode()

    base64_id = base64.urlsafe_b64encode(
        url_bytes
    ).decode().strip("=")

    return base64_id

# ---------------------------------------------------
# GET VT REPORT
# ---------------------------------------------------

def get_virustotal_report(url):

    try:

        # -------------------------------------------
        # ENCODE URL
        # -------------------------------------------

        url_id = url_to_id(url)

        # -------------------------------------------
        # GET EXISTING REPORT
        # -------------------------------------------

        vt_url = (

            f"https://www.virustotal.com/api/v3/urls/{url_id}"
        )

        response = requests.get(

            vt_url,

            headers=headers,

            timeout=10
        )

        # -------------------------------------------
        # REPORT FOUND
        # -------------------------------------------

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

            total = sum(stats.values())

            detection_score = (

                malicious + suspicious
            ) / max(total, 1)

            return {

                "found": True,

                "malicious": malicious,

                "suspicious": suspicious,

                "harmless": harmless,

                "total_engines": total,

                "confidence": round(
                    detection_score,
                    4
                ),

                "status": (

                    "malicious"

                    if detection_score >= 0.30

                    else "safe"
                )
            }

        # -------------------------------------------
        # NOT FOUND -> SUBMIT URL
        # -------------------------------------------

        elif response.status_code == 404:

            submit_url = (
                "https://www.virustotal.com/api/v3/urls"
            )

            submit_response = requests.post(

                submit_url,

                headers=headers,

                data={
                    "url": url
                },

                timeout=10
            )

            if submit_response.status_code in [
                200,
                202
            ]:

                return {

                    "found": False,

                    "status": "unknown",

                    "confidence": 0.0,

                    "message": (
                        "Submitted for scanning"
                    )
                }

        # -------------------------------------------
        # API LIMIT
        # -------------------------------------------

        elif response.status_code == 429:

            return {

                "found": False,

                "status": "rate_limited",

                "confidence": 0.0,

                "message": (
                    "VirusTotal rate limit exceeded"
                )
            }

        # -------------------------------------------
        # OTHER ERRORS
        # -------------------------------------------

        return {

            "found": False,

            "status": "error",

            "confidence": 0.0,

            "message": (
                f"VT Error: {response.status_code}"
            )
        }

    except Exception as e:

        return {

            "found": False,

            "status": "error",

            "confidence": 0.0,

            "message": str(e)
        }