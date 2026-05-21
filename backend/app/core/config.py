import os

from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# SETTINGS
# ---------------------------------------------------

class Settings:

    # ---------------------------------------------------
    # APP CONFIG
    # ---------------------------------------------------

    APP_NAME = "AI Phishing Shield API"

    APP_VERSION = "2.0"

    DEBUG = True

    API_V1_PREFIX = "/api/v1"

    # ---------------------------------------------------
    # DATABASE
    # ---------------------------------------------------

    DATABASE_URL = os.getenv(

        "DATABASE_URL"

    )

    # ---------------------------------------------------
    # JWT AUTH
    # ---------------------------------------------------

    SECRET_KEY = os.getenv(

        "SECRET_KEY",

        "super-secret-key-change-in-production"

    )

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    REFRESH_TOKEN_EXPIRE_DAYS = 7

    # ---------------------------------------------------
    # PASSWORD SECURITY
    # ---------------------------------------------------

    PASSWORD_MIN_LENGTH = 8

    # ---------------------------------------------------
    # API RATE LIMITS
    # ---------------------------------------------------

    FREE_PLAN_DAILY_LIMIT = 100

    PRO_PLAN_DAILY_LIMIT = 5000

    ENTERPRISE_PLAN_LIMIT = 999999

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

        f"{MODEL_DIR}/lgb_model_small.pkl"

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
    # URL SECURITY
    # ---------------------------------------------------

    MAX_URL_LENGTH = 2048

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
    # LOGGING
    # ---------------------------------------------------

    LOG_LEVEL = "INFO"

# ---------------------------------------------------
# SETTINGS INSTANCE
# ---------------------------------------------------

settings = Settings()