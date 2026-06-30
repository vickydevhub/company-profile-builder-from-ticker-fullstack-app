from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.sql import func

from app.database.session import Base


class Profile(Base):

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(String(50), unique=True, nullable=False)

    ticker = Column(String(20), nullable=False)

    status = Column(String(20), nullable=False)

    progress = Column(Integer, default=0)

    profile_json = Column(Text, nullable=True)

    error = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )