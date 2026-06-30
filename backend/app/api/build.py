from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.build import BuildRequest, BuildResponse
from app.services.build_service import BuildService

router = APIRouter(
    prefix="/build",
    tags=["Build"]
)


@router.get("/health")
def health():
    return {
        "status": "Build API Working"
    }


@router.post(
    "",
    response_model=BuildResponse
)
def start_build(
    request: BuildRequest,
    db: Session = Depends(get_db)
):
    service = BuildService(db)

    return service.build_profile(request.ticker)