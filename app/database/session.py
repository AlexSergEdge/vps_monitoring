from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative

from core.config import settings


SQLALCHEMY_DATABASE_URL = settings.POSTGRES_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Alternative way:
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()

@as_declarative()
class Base:
    id: Any
    __name__: str

    # So we don't need to write __tablename__ in each model, it will be taken from model name!
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()