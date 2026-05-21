from fastapi import APIRouter
from fastapi import Depends

# ---------------------------------------------------
# AUTH
# ---------------------------------------------------

from app.auth.dependencies import (
    get_current_user
)

# ---------------------------------------------------
# MODELS
# ---------------------------------------------------

from app.database.models import User

# ---------------------------------------------------
# LOGGER
# ---------------------------------------------------

from app.core.logger import logger

# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

router = APIRouter(

    prefix="/user",

    tags=["User"]

)

# ---------------------------------------------------
# CURRENT USER
# ---------------------------------------------------

@router.get("/me")

def get_me(

    current_user: User = Depends(

        get_current_user

    )

):

    logger.info(

        f"Profile accessed: {current_user.email}"

    )

    return {

        "id": current_user.id,

        "username": current_user.username,

        "email": current_user.email,

        "subscription_plan": current_user.subscription_plan,

        "scans_used": current_user.scans_used,

        "api_key": current_user.api_key

    }

# ---------------------------------------------------
# USER STATS
# ---------------------------------------------------

@router.get("/usage")

def get_usage(

    current_user: User = Depends(

        get_current_user

    )

):

    return {

        "subscription_plan":

            current_user.subscription_plan,

        "scans_used":

            current_user.scans_used

    }