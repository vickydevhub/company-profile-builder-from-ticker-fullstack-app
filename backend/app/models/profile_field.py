from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.database.session import Base


class ProfileField(Base):

    __tablename__ = "profile_fields"

    id = Column(Integer, primary_key=True, index=True)

    profile_id = Column(
        Integer,
        ForeignKey("profiles.id"),
        nullable=False
    )

    section = Column(String(100))

    field = Column(String(100))

    label = Column(String(200))

    value = Column(Text)

    source = Column(Text)

    source_url = Column(Text)

    confidence = Column(Float)

    accepted = Column(Boolean, default=False)