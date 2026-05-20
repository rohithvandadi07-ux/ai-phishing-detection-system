from fastapi import APIRouter

from app.schemas.response_models import HealthResponse

# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

router = APIRouter()

# ---------------------------------------------------
# HEALTH ROUTE
# ---------------------------------------------------

@router.get(

    "/health",

    response_model=HealthResponse,

    tags=["Health"]

)

def health():

    return {

        "status": "healthy"

    }