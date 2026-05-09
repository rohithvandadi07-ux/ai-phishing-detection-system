import sqlite3
from datetime import datetime

DB_PATH = "logs/detections.db"


# ---------------------------------------------------
# CREATE DATABASE + TABLE
# ---------------------------------------------------

def initialize_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS detections (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            url TEXT,

            prediction TEXT,

            risk_score INTEGER,

            risk_level TEXT,

            confidence REAL

        )

    """)

    conn.commit()

    conn.close()


# ---------------------------------------------------
# INSERT DETECTION
# ---------------------------------------------------

def log_detection(
    url,
    prediction,
    risk_score,
    risk_level,
    confidence
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO detections (

            timestamp,
            url,
            prediction,
            risk_score,
            risk_level,
            confidence

        )

        VALUES (?, ?, ?, ?, ?, ?)

    """, (

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        url,

        prediction,

        risk_score,

        risk_level,

        confidence

    ))

    conn.commit()

    conn.close()


# ---------------------------------------------------
# FETCH ALL DETECTIONS
# ---------------------------------------------------

def fetch_detections():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM detections

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows