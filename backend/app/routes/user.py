from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

# ---------------------------------------------------
# AUTH
# ---------------------------------------------------

from app.auth.dependencies import (
    get_current_user
)

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

from app.database.database import get_db

# ---------------------------------------------------
# MODELS
# ---------------------------------------------------

from app.database.models import (
    User,
    ScanHistory
)

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

        "api_key": current_user.api_key,

        "is_active": current_user.is_active,

        "created_at": current_user.created_at

    }

# ---------------------------------------------------
# USER USAGE
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

# ---------------------------------------------------
# USER SCAN HISTORY
# ---------------------------------------------------

@router.get("/history")

def get_scan_history(

    limit: int = Query(10, ge=1, le=100),

    current_user: User = Depends(

        get_current_user

    ),

    db: Session = Depends(get_db)

):

    history = db.query(

        ScanHistory

    ).filter(

        ScanHistory.user_id == current_user.id

    ).order_by(

        ScanHistory.created_at.desc()

    ).limit(limit).all()

    logger.info(

        f"History accessed: {current_user.email}"

    )

    return [

        {

            "id": item.id,

            "url": item.url,

            "prediction": item.prediction,

            "risk_score": item.risk_score,

            "risk_level": item.risk_level,

            "confidence": item.confidence,

            "scan_source": item.scan_source,

            "cached_result": item.cached_result,

            "created_at": item.created_at

        }

        for item in history

    ]

# ---------------------------------------------------
# USER STATS
# ---------------------------------------------------

@router.get("/stats")

def get_user_stats(

    current_user: User = Depends(

        get_current_user

    ),

    db: Session = Depends(get_db)

):

    total_scans = db.query(

        ScanHistory

    ).filter(

        ScanHistory.user_id == current_user.id

    ).count()

    malicious_count = db.query(

        ScanHistory

    ).filter(

        ScanHistory.user_id == current_user.id,

        ScanHistory.prediction == "malicious"

    ).count()

    safe_count = db.query(

        ScanHistory

    ).filter(

        ScanHistory.user_id == current_user.id,

        ScanHistory.prediction == "safe"

    ).count()

    critical_count = db.query(

        ScanHistory

    ).filter(

        ScanHistory.user_id == current_user.id,

        ScanHistory.risk_level == "CRITICAL"

    ).count()

    return {

        "total_scans": total_scans,

        "malicious_detected": malicious_count,

        "safe_urls": safe_count,

        "critical_threats": critical_count,

        "subscription_plan":

            current_user.subscription_plan

    }

# ---------------------------------------------------
# RECENT THREATS
# ---------------------------------------------------

@router.get("/recent-threats")

def recent_threats(

    limit: int = Query(5, ge=1, le=50),

    current_user: User = Depends(

        get_current_user

    ),

    db: Session = Depends(get_db)

):

    threats = db.query(

        ScanHistory

    ).filter(

        ScanHistory.user_id == current_user.id,

        ScanHistory.prediction == "malicious"

    ).order_by(

        ScanHistory.created_at.desc()

    ).limit(limit).all()

    return [

        {

            "url": item.url,

            "risk_score": item.risk_score,

            "risk_level": item.risk_level,

            "created_at": item.created_at

        }

        for item in threats

    ]