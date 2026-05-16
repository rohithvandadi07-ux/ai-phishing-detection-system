import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# DATABASE URL
# ---------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

# ---------------------------------------------------
# SAFETY CHECK
# ---------------------------------------------------

if not DATABASE_URL:

    raise ValueError(

        "DATABASE_URL not found in environment variables"

    )

# ---------------------------------------------------
# SQLALCHEMY ENGINE
# ---------------------------------------------------

engine = create_engine(

    DATABASE_URL

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
# INITIALIZE DATABASE
# ---------------------------------------------------

def initialize_database():

    Base.metadata.create_all(bind=engine)

# ---------------------------------------------------
# TEMP LOG FUNCTION
# ---------------------------------------------------

def log_detection(

    url,
    prediction,
    risk_score,
    risk_level,
    confidence

):

    print(

        f"[SUPABASE LOG] "
        f"{url} | "
        f"{prediction}"

    )