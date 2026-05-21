from pydantic import BaseModel

from typing import List
from typing import Dict
from typing import Any
from typing import Optional

# ---------------------------------------------------
# TOKEN RESPONSE
# ---------------------------------------------------

class TokenResponse(BaseModel):

    access_token: str

    token_type: str

# ---------------------------------------------------
# USER RESPONSE
# ---------------------------------------------------

class UserResponse(BaseModel):

    id: int

    username: str

    email: str

    subscription_plan: str

    scans_used: int

    api_key: Optional[str] = None

    class Config:

        from_attributes = True

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

    ai_engine: Dict[str, Any]

# ---------------------------------------------------
# HEALTH RESPONSE
# ---------------------------------------------------

class HealthResponse(BaseModel):

    status: str