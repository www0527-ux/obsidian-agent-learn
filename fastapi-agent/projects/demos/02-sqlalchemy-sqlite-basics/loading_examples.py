from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from db import engine
from models import User


def list_users_lazy() -> list[User]:
    print("\n--- Lazy loading: query users, then access user.records in loop ---")
    with Session(engine) as session:
        users = list(session.scalars(select(User).order_by(User.id)).all())
        for user in users:
            print(f"User {user.id} {user.name}")
            for record in user.records:
                print(f"  - {record.title}")
        return users


def list_users_with_selectinload() -> list[User]:
    print("\n--- selectinload: query users, then batch-load records with IN (...) ---")
    with Session(engine) as session:
        stmt = (
            select(User)
            .options(selectinload(User.records))
            .order_by(User.id)
        )
        users = list(session.scalars(stmt).all())
        for user in users:
            print(f"User {user.id} {user.name}")
            for record in user.records:
                print(f"  - {record.title}")
        return users


def list_users_with_joinedload() -> list[User]:
    print("\n--- joinedload: query users and records with JOIN-like eager loading ---")
    with Session(engine) as session:
        stmt = (
            select(User)
            .options(joinedload(User.records))
            .order_by(User.id)
        )
        users = list(session.scalars(stmt).unique().all())
        for user in users:
            print(f"User {user.id} {user.name}")
            for record in user.records:
                print(f"  - {record.title}")
        return users

