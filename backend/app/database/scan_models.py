from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

from app.database.database import Base

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

        nullable=False

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

        DateTime,

        default=datetime.utcnow

    )