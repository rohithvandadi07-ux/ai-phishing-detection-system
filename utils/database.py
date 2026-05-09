import os

from dotenv import load_dotenv

from sqlalchemy import (

    create_engine,
    text

)

from datetime import datetime

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# ---------------------------------------------------
# CREATE ENGINE
# ---------------------------------------------------

engine = create_engine(
    DATABASE_URL
)

# ---------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------

def initialize_database():

    with engine.connect() as conn:

        conn.execute(text("""

            CREATE TABLE IF NOT EXISTS detections (

                id SERIAL PRIMARY KEY,

                timestamp TEXT,

                url TEXT,

                prediction TEXT,

                risk_score INTEGER,

                risk_level TEXT,

                confidence FLOAT

            )

        """))

        conn.commit()

# ---------------------------------------------------
# LOG DETECTION
# ---------------------------------------------------

def log_detection(

    url,
    prediction,
    risk_score,
    risk_level,
    confidence

):

    with engine.connect() as conn:

        conn.execute(text("""

            INSERT INTO detections (

                timestamp,
                url,
                prediction,
                risk_score,
                risk_level,
                confidence

            )

            VALUES (

                :timestamp,
                :url,
                :prediction,
                :risk_score,
                :risk_level,
                :confidence

            )

        """), {

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "url": url,

            "prediction": prediction,

            "risk_score": risk_score,

            "risk_level": risk_level,

            "confidence": confidence

        })

        conn.commit()

# ---------------------------------------------------
# FETCH DETECTIONS
# ---------------------------------------------------

def fetch_detections():

    with engine.connect() as conn:

        result = conn.execute(text("""

            SELECT *

            FROM detections

            ORDER BY id DESC

        """))

        return result.fetchall()