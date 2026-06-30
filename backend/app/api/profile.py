from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.profile_service import ProfileService

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/health")
def health():
    return {
        "status": "Profile API Working"
    }


@router.get("/{job_id}")
def get_profile(
    job_id: str,
    db: Session = Depends(get_db)
):
    service = ProfileService(db)

    return service.get_profile(job_id)

@router.post("/save/{job_id}")
def save_profile(
    job_id: str,
    profile: list = Body(...),
    db: Session = Depends(get_db)
):
    service = ProfileService(db)

    return service.save_profile(
        job_id,
        profile
    )


@router.get("/saved/{job_id}")
def saved_profile(
    job_id: str,
    db: Session = Depends(get_db)
):
    service = ProfileService(db)

    return service.get_saved_profile(job_id)