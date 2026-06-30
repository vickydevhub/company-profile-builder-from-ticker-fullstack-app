from sqlalchemy.orm import Session

from app.core.exceptions import ValidationException
from app.core.logger import logger
from app.repositories.profile_repository import ProfileRepository
from app.services.stub_service import stub_service


class ProfileService:

    def __init__(self, db: Session):
        self.repository = ProfileRepository(db)

    def get_profile(self, job_id: str):

        if not job_id:
            raise ValidationException("Job ID is required.")

        logger.info(f"Fetching profile for job: {job_id}")

        # Check if job exists in database
        profile = self.repository.get_by_job_id(job_id)

        if not profile:
            raise ValidationException("Job not found.")

        # Fetch latest status from stub
        response = stub_service.get_build_status(job_id)

        # Update database
        self.repository.update_status(
            job_id=job_id,
            status=response.get("status"),
            progress=response.get("progress", 0),
            profile_data=response.get("profile"),
            error=response.get("error"),
        )

        return response
    
    def save_profile(self, job_id: str, profile):
        return self.repository.save_reviewed_profile(
            job_id,
            profile
        )


    def get_saved_profile(self, job_id: str):
        return self.repository.get_saved_profile(job_id)