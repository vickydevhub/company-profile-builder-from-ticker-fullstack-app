from sqlalchemy.orm import Session

from app.core.exceptions import ValidationException
from app.core.logger import logger
from app.repositories.profile_repository import ProfileRepository
from app.services.stub_service import stub_service


class BuildService:

    def __init__(self, db: Session):
        self.repository = ProfileRepository(db)

    def build_profile(self, ticker: str):

        ticker = ticker.strip().upper()

        if not ticker:
            raise ValidationException("Ticker is required.")

        logger.info(f"Starting build for ticker: {ticker}")

        response = stub_service.start_build(ticker)

        self.repository.create(
            job_id=response["job_id"],
            ticker=ticker,
            status="running",
            progress=0,
        )

        logger.info(f"Job created successfully: {response['job_id']}")

        return response