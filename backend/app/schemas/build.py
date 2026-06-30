from pydantic import BaseModel, Field


class BuildRequest(BaseModel):
    ticker: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Stock ticker symbol"
    )


class BuildResponse(BaseModel):
    job_id: str