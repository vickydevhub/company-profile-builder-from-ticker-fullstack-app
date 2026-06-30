import requests

from app.config import settings
from app.core.exceptions import StubServiceException
from app.core.logger import logger


class StubService:
    """Handles communication with the external Profile Builder Stub."""

    def start_build(self, ticker: str):
        url = f"{settings.STUB_BASE_URL}/build"

        try:
            logger.info(f"Starting build for ticker: {ticker}")

            response = requests.post(
                url,
                json={"ticker": ticker},
                timeout=10
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.exception("Failed to start build")
            raise StubServiceException(str(e))

    def get_build_status(self, job_id: str):
        url = f"{settings.STUB_BASE_URL}/build/{job_id}"

        try:
            logger.info(f"Checking build status: {job_id}")

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.exception("Failed to fetch build status")
            raise StubServiceException(str(e))


stub_service = StubService()