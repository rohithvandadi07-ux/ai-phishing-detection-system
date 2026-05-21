from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# ---------------------------------------------------
# URL SCAN REQUEST
# ---------------------------------------------------

class URLRequest(BaseModel):

    url: str = Field(

        ...,

        min_length=5,

        max_length=2048,

        description="URL to scan"

    )

# ---------------------------------------------------
# USER SIGNUP REQUEST
# ---------------------------------------------------

class UserSignupRequest(BaseModel):

    username: str = Field(

        ...,

        min_length=3,

        max_length=50

    )

    email: EmailStr

    password: str = Field(

        ...,

        min_length=8,

        max_length=128

    )

# ---------------------------------------------------
# USER LOGIN REQUEST
# ---------------------------------------------------

class UserLoginRequest(BaseModel):

    email: EmailStr

    password: str

# ---------------------------------------------------
# TOKEN RESPONSE
# ---------------------------------------------------

class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"

# ---------------------------------------------------
# USER RESPONSE
# ---------------------------------------------------

class UserResponse(BaseModel):

    id: int

    username: str

    email: str

    subscription_plan: str

    scans_used: int

    class Config:

        from_attributes = True