from sqlalchemy.orm import Session

from app.database.session import Base, SessionLocal, engine


def init_db():
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Database session dependency.
    """
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()