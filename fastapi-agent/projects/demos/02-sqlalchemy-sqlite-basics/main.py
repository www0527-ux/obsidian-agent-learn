from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


engine = create_engine("sqlite:///demo.db", echo=False)


def reset_database() -> None:
    Base.metadata.drop_all(engine)#清空旧表
    Base.metadata.create_all(engine)


def insert_user() -> User:
    with Session(engine) as session:
        user = User(username="alice", email="alice@example.com")
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"Inserted user: id={user.id}, username={user.username}")
        return user


def query_user_by_username(username: str) -> User | None:
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        user = session.scalar(stmt)
        if user is None:
            return None
        print(f"Queried user: id={user.id}, username={user.username}, email={user.email}")
        return user


def list_users() -> list[User]:
    with Session(engine) as session:
        users = list(session.scalars(select(User).order_by(User.id)))
        print("All users:")
        for user in users:
            print(f"- {user.id} {user.username} {user.email}")
        return users


def main() -> None:
    reset_database()
    insert_user()
    query_user_by_username("alice")
    list_users()


if __name__ == "__main__":
    main()

