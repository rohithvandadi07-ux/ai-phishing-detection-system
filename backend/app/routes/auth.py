from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

from app.database.database import get_db

# ---------------------------------------------------
# AUTH SERVICE
# ---------------------------------------------------

from app.auth.auth_service import (
    create_user,
    login_user
)

# ---------------------------------------------------
# SCHEMAS
# ---------------------------------------------------

from app.schemas.request_models import (
    UserSignupRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse
)

# ---------------------------------------------------
# LOGGER
# ---------------------------------------------------

from app.core.logger import logger

# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)

# ---------------------------------------------------
# SIGNUP ROUTE
# ---------------------------------------------------

@router.post(

    "/signup",

    response_model=UserResponse

)

def signup(

    request: UserSignupRequest,

    db: Session = Depends(get_db)

):

    user, error = create_user(

        db=db,

        username=request.username,

        email=request.email,

        password=request.password

    )

    if error:

        logger.warning(

            f"Signup failed: {error}"

        )

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=error

        )

    logger.info(

        f"User created: {request.email}"

    )

    return user

# ---------------------------------------------------
# LOGIN ROUTE
# ---------------------------------------------------

@router.post(

    "/login",

    response_model=TokenResponse

)

def login(

    request: UserLoginRequest,

    db: Session = Depends(get_db)

):

    token_data = login_user(

        db=db,

        email=request.email,

        password=request.password

    )

    if not token_data:

        logger.warning(

            f"Failed login attempt: {request.email}"

        )

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid email or password"

        )

    logger.info(

        f"Successful login: {request.email}"

    )

    return token_data