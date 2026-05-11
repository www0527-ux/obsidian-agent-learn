from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


engine = create_engine("sqlite:///practice.db", echo=True)


class Base(DeclarativeBase):
    pass


def reset_database() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

