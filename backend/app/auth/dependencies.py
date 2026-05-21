from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

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
# SECURITY
# ---------------------------------------------------

from app.auth.security import verify_access_token

# ---------------------------------------------------
# LOGGER
# ---------------------------------------------------

from app.core.logger import logger

# ---------------------------------------------------
# OAUTH2 SCHEME
# ---------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(

    tokenUrl="/auth/login"

)

# ---------------------------------------------------
# GET CURRENT USER
# ---------------------------------------------------

def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    credentials_exception = HTTPException(

        status_code=status.HTTP_401_UNAUTHORIZED,

        detail="Invalid authentication credentials",

        headers={

            "WWW-Authenticate": "Bearer"

        }

    )

    payload = verify_access_token(token)

    if payload is None:

        logger.warning(

            "Invalid JWT token"

        )

        raise credentials_exception

    user_email = payload.get("sub")

    if user_email is None:

        raise credentials_exception

    user = db.query(User).filter(

        User.email == user_email

    ).first()

    if user is None:

        raise credentials_exception

    return user