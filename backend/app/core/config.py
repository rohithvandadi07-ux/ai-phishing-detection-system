import os

from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# PROJECT CONFIGURATION
# ---------------------------------------------------

class Settings:

    # ---------------------------------------------------
    # APP
    # ---------------------------------------------------

    APP_NAME = "AI Phishing Shield API"

    APP_VERSION = "2.0"

    DEBUG = True

    # ---------------------------------------------------
    # DATABASE
    # ---------------------------------------------------

    DATABASE_URL = os.getenv("DATABASE_URL")

    # ---------------------------------------------------
    # SECURITY
    # ---------------------------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-in-production"
    )

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    # ---------------------------------------------------
    # API KEYS
    # ---------------------------------------------------

    VIRUSTOTAL_API_KEY = os.getenv(
        "VIRUSTOTAL_API_KEY",
        ""
    )

    PHISHTANK_API_KEY = os.getenv(
        "PHISHTANK_API_KEY",
        ""
    )

    # ---------------------------------------------------
    # MODEL PATHS
    # ---------------------------------------------------

    MODEL_DIR = "models"

    RF_MODEL_PATH = (
        f"{MODEL_DIR}/rf_model.pkl"
    )

    LGB_MODEL_PATH = (
        f"{MODEL_DIR}/lgb_model.pkl"
    )

    CNN_MODEL_PATH = (
        f"{MODEL_DIR}/cnn_model.pt"
    )

    SCALER_PATH = (
        f"{MODEL_DIR}/scaler.pkl"
    )

    # ---------------------------------------------------
    # CACHE
    # ---------------------------------------------------

    CACHE_EXPIRY_SECONDS = 300

    # ---------------------------------------------------
    # SAFE DOMAINS
    # ---------------------------------------------------

    SAFE_DOMAINS = {

        "google.com",
        "github.com",
        "amazon.com",
        "amazon.in",
        "microsoft.com",
        "apple.com",
        "linkedin.com",
        "stackoverflow.com"

    }


# ---------------------------------------------------
# SETTINGS INSTANCE
# ---------------------------------------------------

settings = Settings()