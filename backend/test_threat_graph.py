from app.services.threat_graph_engine import (
    classify_threat_family
)

urls = [

    "https://google.com",

    "https://g00gle-login.com",

    "https://paypal-secure.xyz",

    "https://amazon-verification.net",

    "https://micr0soft-login.com",

    "http://free-bitcoin-login-secure.xyz"

]

for url in urls:

    print("=" * 70)

    print(url)

    print(
        classify_threat_family(url)
    )