import json
from typing import Optional

from sqlalchemy.orm import Session

from app.models.profile import Profile


class ProfileRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        job_id: str,
        ticker: str,
        status: str = "running",
        progress: int = 0,
    ) -> Profile:

        profile = Profile(
            job_id=job_id,
            ticker=ticker,
            status=status,
            progress=progress,
        )

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile

    def get_by_job_id(self, job_id: str) -> Optional[Profile]:

        return (
            self.db.query(Profile)
            .filter(Profile.job_id == job_id)
            .first()
        )

    def update_status(
        self,
        job_id: str,
        status: str,
        progress: int,
        profile_data: dict | None = None,
        error: str | None = None,
    ) -> Optional[Profile]:

        profile = self.get_by_job_id(job_id)

        if not profile:
            return None

        profile.status = status
        profile.progress = progress

        if profile_data is not None:
            profile.profile_json = json.dumps(profile_data)

        if error is not None:
            profile.error = error

        self.db.commit()
        self.db.refresh(profile)

        return profile

    def update_progress(
        self,
        job_id: str,
        progress: int,
    ) -> Optional[Profile]:

        profile = self.get_by_job_id(job_id)

        if not profile:
            return None

        profile.progress = progress

        self.db.commit()
        self.db.refresh(profile)

        return profile

    def delete(self, job_id: str) -> bool:

        profile = self.get_by_job_id(job_id)

        if not profile:
            return False

        self.db.delete(profile)
        self.db.commit()

        return True

    def get_all(self):

        return (
            self.db.query(Profile)
            .order_by(Profile.created_at.desc())
            .all()
        )
    
    def save_reviewed_profile(self, job_id: str, profile_data):
        profile = self.get_by_job_id(job_id)

        if not profile:
            return None

        profile.profile_json = json.dumps(profile_data)
        self.db.commit()
        self.db.refresh(profile)

        return profile


    def get_saved_profile(self, job_id: str):
        profile = self.get_by_job_id(job_id)

        if not profile:
            return None

        if profile.profile_json:
            profile.profile_json = json.loads(profile.profile_json)

        return profile