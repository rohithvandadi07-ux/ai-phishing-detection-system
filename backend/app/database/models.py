from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.database.database import Base

# ---------------------------------------------------
# USER MODEL
# ---------------------------------------------------

class User(Base):

    __tablename__ = "users"

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )

    username = Column(

        String,

        unique=True,

        nullable=False

    )

    email = Column(

        String,

        unique=True,

        nullable=False

    )

    hashed_password = Column(

        String,

        nullable=False

    )

    api_key = Column(

        String,

        unique=True,

        nullable=True

    )

    subscription_plan = Column(

        String,

        default="free"

    )

    scans_used = Column(

        Integer,

        default=0

    )

    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )

# ---------------------------------------------------
# DETECTION LOG MODEL
# ---------------------------------------------------

class DetectionLog(Base):

    __tablename__ = "detection_logs"

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )

    url = Column(

        String,

        nullable=False

    )

    prediction = Column(

        String,

        nullable=False

    )

    risk_score = Column(

        Integer,

        nullable=False

    )

    risk_level = Column(

        String,

        nullable=False

    )

    confidence = Column(

        Float,

        nullable=False

    )

    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )