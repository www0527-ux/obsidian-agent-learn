from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


# Demo URL. In a real app, read this from settings or environment variables.
DATABASE_URL = "sqlite:///alembic_template.db"

engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass
