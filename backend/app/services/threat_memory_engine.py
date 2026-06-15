import json
import os

MEMORY_FILE = "threat_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    try:

        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    except Exception:
        return {}


def save_memory(data):

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def remember_threat(
    family,
    domain
):

    if family == "unknown":
        return

    memory = load_memory()

    if family not in memory:

        memory[family] = []

    if domain not in memory[family]:

        memory[family].append(domain)

    save_memory(memory)


def lookup_family(family):

    memory = load_memory()

    return memory.get(
        family,
        []
    )