from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.health import router as health_router
from app.routes.predict import router as predict_router

from app.database.database import initialize_database

from app.core.logger import logger

# ---------------------------------------------------
# FASTAPI INIT
# ---------------------------------------------------

app = FastAPI(

    title="AI Phishing Shield API",

    version="2.0"

)

# ---------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------

initialize_database()

logger.info("Database initialized")

# ---------------------------------------------------
# CORS CONFIG
# ---------------------------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# ---------------------------------------------------
# INCLUDE ROUTES
# ---------------------------------------------------

app.include_router(health_router)

app.include_router(predict_router)

# ---------------------------------------------------
# ROOT ROUTE
# ---------------------------------------------------

@app.get("/")

def home():

    logger.info("Root endpoint accessed")

    return {

        "message":

        "AI Phishing Shield API Running"

    }