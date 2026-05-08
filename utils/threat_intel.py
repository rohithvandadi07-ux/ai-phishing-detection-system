import requests

# Replace with your actual VirusTotal API key
VT_API_KEY = "42b0d0a9ef511721ef627a0f5dd498fd5b06d2721e19631931030e689ef7eb90"


def check_virustotal(url):

    try:

        headers = {
            "x-apikey": VT_API_KEY
        }

        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )

        if response.status_code != 200:
            return {
                "malicious": False,
                "score": 0,
                "source": "VirusTotal Error"
            }

        url_id = response.json()["data"]["id"]

        analysis_url = f"https://www.virustotal.com/api/v3/analyses/{url_id}"

        analysis_response = requests.get(
            analysis_url,
            headers=headers
        )

        result = analysis_response.json()

        stats = result["data"]["attributes"]["stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)

        total_score = malicious + suspicious

        return {
            "malicious": total_score > 0,
            "score": total_score,
            "source": "VirusTotal"
        }

    except Exception as e:

        return {
            "malicious": False,
            "score": 0,
            "source": str(e)
        }