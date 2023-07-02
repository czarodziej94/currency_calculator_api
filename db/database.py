from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from db.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./currency.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
