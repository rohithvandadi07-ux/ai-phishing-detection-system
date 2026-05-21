from datetime import datetime
from datetime import timedelta

from jose import JWTError
from jose import jwt

from passlib.context import CryptContext

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

from app.core.config import settings

# ---------------------------------------------------
# PASSWORD HASHING
# ---------------------------------------------------

pwd_context = CryptContext(

    schemes=["bcrypt"],

    deprecated="auto"

)

# ---------------------------------------------------
# HASH PASSWORD
# ---------------------------------------------------

def hash_password(password: str):

    return pwd_context.hash(password)

# ---------------------------------------------------
# VERIFY PASSWORD
# ---------------------------------------------------

def verify_password(

    plain_password: str,

    hashed_password: str

):

    return pwd_context.verify(

        plain_password,

        hashed_password

    )

# ---------------------------------------------------
# CREATE ACCESS TOKEN
# ---------------------------------------------------

def create_access_token(

    data: dict,

    expires_delta: timedelta = None

):

    to_encode = data.copy()

    if expires_delta:

        expire = datetime.utcnow() + expires_delta

    else:

        expire = datetime.utcnow() + timedelta(

            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES

        )

    to_encode.update({

        "exp": expire

    })

    encoded_jwt = jwt.encode(

        to_encode,

        settings.SECRET_KEY,

        algorithm=settings.ALGORITHM

    )

    return encoded_jwt

# ---------------------------------------------------
# VERIFY ACCESS TOKEN
# ---------------------------------------------------

def verify_access_token(token: str):

    try:

        payload = jwt.decode(

            token,

            settings.SECRET_KEY,

            algorithms=[settings.ALGORITHM]

        )

        return payload

    except JWTError:

        return None