from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logger import logger

from app.core.constants import *

# ---------------------------------------------------
# GLOBAL EXCEPTION HANDLER
# ---------------------------------------------------

async def global_exception_handler(

    request: Request,

    exc: Exception

):

    logger.error(

        f"Unhandled Exception: {str(exc)}"

    )

    return JSONResponse(

        status_code=500,

        content={

            "prediction": PREDICTION_ERROR,

            "confidence": 0.0,

            "risk_score": 0,

            "risk_level": RISK_HIGH,

            "inference_time": 0.0,

            "reasons": [

                "Internal server error"

            ],

            "ai_engine": {}

        }

    )