from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

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
        nullable=False,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    api_key = Column(
        String,
        unique=True,
        nullable=True,
        index=True
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
    # RELATIONSHIP
    # ---------------------------------------------------

    scan_history = relationship(
        "ScanHistory",
        back_populates="user",
        cascade="all, delete-orphan"
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
        nullable=False,
        index=True
    )

    prediction = Column(
        String,
        nullable=False,
        index=True
    )

    risk_score = Column(
        Integer,
        nullable=False
    )

    risk_level = Column(
        String,
        nullable=False,
        index=True
    )

    confidence = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )

# ---------------------------------------------------
# SCAN HISTORY MODEL
# ---------------------------------------------------

class ScanHistory(Base):

    __tablename__ = "scan_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    url = Column(
        Text,
        nullable=False
    )

    prediction = Column(
        String,
        nullable=False,
        index=True
    )

    risk_score = Column(
        Integer,
        nullable=False,
        index=True
    )

    risk_level = Column(
        String,
        nullable=False,
        index=True
    )

    confidence = Column(
        Float,
        nullable=False
    )

    scan_source = Column(
        String,
        default="dashboard"
    )

    cached_result = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )

    # ---------------------------------------------------
    # RELATIONSHIP
    # ---------------------------------------------------

    user = relationship(
        "User",
        back_populates="scan_history"
    )