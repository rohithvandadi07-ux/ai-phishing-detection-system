import json
import os

MEMORY_FILE = "threat_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def analyze_campaign(threat_family):

    memory = load_memory()

    domains = memory.get(
        threat_family,
        []
    )

    count = len(domains)

    if count >= 20:
        level = "ACTIVE"

    elif count >= 10:
        level = "GROWING"

    elif count >= 3:
        level = "EMERGING"

    else:
        level = "NEW"

    return {

        "campaign": threat_family,

        "known_domains": count,

        "campaign_level": level

    }