from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

from app.database.database import get_db

# ---------------------------------------------------
# MODELS
# ---------------------------------------------------

from app.database.models import User

# ---------------------------------------------------
# AUTH SERVICE
# ---------------------------------------------------

from app.auth.auth_service import (
    create_user
)

# ---------------------------------------------------
# SECURITY
# ---------------------------------------------------

from app.auth.security import (
    verify_password,
    create_access_token
)

# ---------------------------------------------------
# SCHEMAS
# ---------------------------------------------------

from app.schemas.request_models import (
    UserSignupRequest
)

from app.schemas.response_models import (
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

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(

        User.email == form_data.username

    ).first()

    if not user:

        logger.warning(

            f"Failed login attempt: {form_data.username}"

        )

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid email or password"

        )

    # ---------------------------------------------------
    # PASSWORD VERIFICATION
    # ---------------------------------------------------

    if not verify_password(

        form_data.password,

        user.hashed_password

    ):

        logger.warning(

            f"Invalid password attempt: {form_data.username}"

        )

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid email or password"

        )

    # ---------------------------------------------------
    # CREATE JWT TOKEN
    # ---------------------------------------------------

    access_token = create_access_token(

        data={

            "sub": user.email,

            "user_id": user.id

        }

    )

    logger.info(

        f"Successful login: {user.email}"

    )

    return {

        "access_token": access_token,

        "token_type": "bearer"

    }