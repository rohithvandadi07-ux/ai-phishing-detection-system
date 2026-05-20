import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ---------------------------------------------------
# CORE CONFIG
# ---------------------------------------------------

from app.core.config import settings

# ---------------------------------------------------
# LOGGER
# ---------------------------------------------------

from app.core.logger import logger

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# DATABASE URL
# ---------------------------------------------------

DATABASE_URL = settings.DATABASE_URL

# ---------------------------------------------------
# SAFETY CHECK
# ---------------------------------------------------

if not DATABASE_URL:

    logger.error(

        "DATABASE_URL missing from environment variables"

    )

    raise ValueError(

        "DATABASE_URL not found in environment variables"

    )

# ---------------------------------------------------
# SQLALCHEMY ENGINE
# ---------------------------------------------------

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True,

    pool_recycle=300

)

# ---------------------------------------------------
# SESSION
# ---------------------------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)

# ---------------------------------------------------
# BASE
# ---------------------------------------------------

Base = declarative_base()

# ---------------------------------------------------
# DATABASE SESSION DEPENDENCY
# ---------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

# ---------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------

def initialize_database():

    try:

        Base.metadata.create_all(bind=engine)

        logger.info(

            "Database initialized successfully"

        )

    except Exception as e:

        logger.error(

            f"Database initialization failed: {str(e)}"

        )

        raise e

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

    logger.info(

        f"[SCAN] "
        f"{url} | "
        f"{prediction} | "
        f"Risk={risk_score} | "
        f"Level={risk_level} | "
        f"Confidence={confidence}"

    )