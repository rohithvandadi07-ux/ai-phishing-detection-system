from pydantic import BaseModel

from typing import List, Dict


# ---------------------------------------------------
# AI ENGINE RESPONSE
# ---------------------------------------------------

class AIEngineResponse(BaseModel):

    lgb_probability: float

    rf_probability: float

    hybrid_probability: float

    semantic_score: float

    semantic_confidence: float


# ---------------------------------------------------
# PREDICTION RESPONSE
# ---------------------------------------------------

class PredictionResponse(BaseModel):

    prediction: str

    confidence: float

    risk_score: int

    risk_level: str

    inference_time: float

    reasons: List[str]

    ai_engine: Dict


# ---------------------------------------------------
# HEALTH RESPONSE
# ---------------------------------------------------

class HealthResponse(BaseModel):

    status: str