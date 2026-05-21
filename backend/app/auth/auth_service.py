import secrets

from sqlalchemy.orm import Session

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

from app.database.models import User

# ---------------------------------------------------
# SECURITY
# ---------------------------------------------------

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

# ---------------------------------------------------
# LOGGER
# ---------------------------------------------------

from app.core.logger import logger

# ---------------------------------------------------
# CREATE API KEY
# ---------------------------------------------------

def generate_api_key():

    return secrets.token_hex(32)

# ---------------------------------------------------
# FIND USER BY EMAIL
# ---------------------------------------------------

def get_user_by_email(

    db: Session,

    email: str

):

    return db.query(User).filter(

        User.email == email

    ).first()

# ---------------------------------------------------
# FIND USER BY USERNAME
# ---------------------------------------------------

def get_user_by_username(

    db: Session,

    username: str

):

    return db.query(User).filter(

        User.username == username

    ).first()

# ---------------------------------------------------
# CREATE USER
# ---------------------------------------------------

def create_user(

    db: Session,

    username: str,

    email: str,

    password: str

):

    existing_email = get_user_by_email(

        db,
        email

    )

    if existing_email:

        return None, "Email already registered"

    existing_username = get_user_by_username(

        db,
        username

    )

    if existing_username:

        return None, "Username already taken"

    hashed_pw = hash_password(password)

    api_key = generate_api_key()

    new_user = User(

        username=username,

        email=email,

        hashed_password=hashed_pw,

        api_key=api_key

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    logger.info(

        f"New user registered: {email}"

    )

    return new_user, None

# ---------------------------------------------------
# AUTHENTICATE USER
# ---------------------------------------------------

def authenticate_user(

    db: Session,

    email: str,

    password: str

):

    user = get_user_by_email(

        db,
        email

    )

    if not user:

        return None

    if not verify_password(

        password,
        user.hashed_password

    ):

        return None

    return user

# ---------------------------------------------------
# LOGIN USER
# ---------------------------------------------------

def login_user(

    db: Session,

    email: str,

    password: str

):

    user = authenticate_user(

        db,
        email,
        password

    )

    if not user:

        return None

    access_token = create_access_token(

        data={

            "sub": user.email,

            "user_id": user.id

        }

    )

    logger.info(

        f"User logged in: {email}"

    )

    return {

        "access_token": access_token,

        "token_type": "bearer"

    }