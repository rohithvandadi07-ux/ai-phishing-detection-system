import csv
import os
from datetime import datetime

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "detections.csv")


def initialize_logger():

    os.makedirs(LOG_FOLDER, exist_ok=True)

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, mode="w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "url",
                "prediction",
                "risk_score",
                "risk_level",
                "confidence"
            ])


def log_detection(
    url,
    prediction,
    risk_score,
    risk_level,
    confidence
):

    initialize_logger()

    with open(LOG_FILE, mode="a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            url,
            prediction,
            risk_score,
            risk_level,
            confidence
        ])