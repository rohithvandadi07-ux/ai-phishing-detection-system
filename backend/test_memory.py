from app.services.threat_memory_engine import (
    remember_threat,
    lookup_family
)

remember_threat(
    "google-phishing",
    "g00gle-login.com"
)

remember_threat(
    "google-phishing",
    "g00gle-verify.net"
)

print(
    lookup_family(
        "google-phishing"
    )
)