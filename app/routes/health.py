from fastapi import APIRouter

router = APIRouter()

# ---------------------------------------------------
# HEALTH ROUTE
# ---------------------------------------------------

@router.get("/health")

def health():

    return {

        "status": "healthy",

        "api": "running",

        "database": "connected"

    }
