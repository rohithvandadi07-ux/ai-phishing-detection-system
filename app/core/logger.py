import csv
import os
import logging

from datetime import datetime

# ---------------------------------------------------
# LOG DIRECTORY
# ---------------------------------------------------

LOG_FOLDER = "logs"

LOG_FILE = os.path.join(
    LOG_FOLDER,
    "detections.csv"
)

APP_LOG_FILE = os.path.join(
    LOG_FOLDER,
    "app.log"
)

# ---------------------------------------------------
# CREATE LOG DIRECTORY
# ---------------------------------------------------

os.makedirs(
    LOG_FOLDER,
    exist_ok=True
)

# ---------------------------------------------------
# PYTHON LOGGER CONFIG
# ---------------------------------------------------

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s",

    handlers=[

        logging.FileHandler(
            APP_LOG_FILE
        ),

        logging.StreamHandler()

    ]
)

# ---------------------------------------------------
# LOGGER INSTANCE
# ---------------------------------------------------

logger = logging.getLogger(
    "phishing-api"
)

# ---------------------------------------------------
# CSV LOGGER INITIALIZATION
# ---------------------------------------------------

def initialize_logger():

    if not os.path.exists(LOG_FILE):

        with open(
            LOG_FILE,
            mode="w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                "timestamp",

                "url",

                "prediction",

                "risk_score",

                "risk_level",

                "confidence"

            ])

# ---------------------------------------------------
# DETECTION LOGGER
# ---------------------------------------------------

def log_detection(

    url,
    prediction,
    risk_score,
    risk_level,
    confidence

):

    initialize_logger()

    with open(
        LOG_FILE,
        mode="a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            url,

            prediction,

            risk_score,

            risk_level,

            confidence

        ])

    logger.info(

        f"{url} -> {prediction} | "
        f"Risk={risk_score} | "
        f"Level={risk_level}"

    )

# ---------------------------------------------------
# STARTUP LOG
# ---------------------------------------------------

logger.info(
    "Logger initialized successfully"
)