from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------
# RATE LIMITING
# ---------------------------------------------------

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

# ---------------------------------------------------
# CORE CONFIG
# ---------------------------------------------------

from app.core.config import settings

# ---------------------------------------------------
# RATE LIMITER
# ---------------------------------------------------

from app.core.rate_limiter import limiter

# ---------------------------------------------------
# LOGGER
# ---------------------------------------------------

from app.core.logger import logger

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

from app.database.database import initialize_database

# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------

from app.routes.health import router as health_router
from app.routes.predict import router as predict_router

# ---------------------------------------------------
# GLOBAL ERROR HANDLER
# ---------------------------------------------------

from app.middleware.error_handler import (
    global_exception_handler
)

# ---------------------------------------------------
# SECURITY HEADERS MIDDLEWARE
# ---------------------------------------------------

from app.middleware.security_headers import (
    SecurityHeadersMiddleware
)

# ---------------------------------------------------
# FASTAPI INIT
# ---------------------------------------------------

app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION

)

# ---------------------------------------------------
# RATE LIMITER
# ---------------------------------------------------

app.state.limiter = limiter

app.add_exception_handler(

    RateLimitExceeded,

    _rate_limit_exceeded_handler

)

app.add_middleware(

    SlowAPIMiddleware

)

# ---------------------------------------------------
# GLOBAL EXCEPTION HANDLER
# ---------------------------------------------------

app.add_exception_handler(

    Exception,

    global_exception_handler

)

# ---------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------

initialize_database()

logger.info("Database initialized")

# ---------------------------------------------------
# SECURITY HEADERS MIDDLEWARE
# ---------------------------------------------------

app.add_middleware(

    SecurityHeadersMiddleware

)

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

        f"{settings.APP_NAME} Running"

    }