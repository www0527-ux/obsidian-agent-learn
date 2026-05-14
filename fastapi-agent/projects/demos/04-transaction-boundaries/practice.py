from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import engine, reset_database
from models import LearningRecord, User


def print_database_state(label: str) -> None:
    print(f"\n--- {label} ---")
    with Session(engine) as session:
        users = list(session.scalars(select(User).order_by(User.id)))
        records = list(session.scalars(select(LearningRecord).order_by(LearningRecord.id)))

        print("users:")
        for user in users:
            print(f"  id={user.id}, name={user.name}")
        if not users:
            print("  <empty>")

        print("learning_records:")
        for record in records:
            print(
                f"  id={record.id}, user_id={record.user_id}, "
                f"title={record.title}, content={record.content}"
            )
        if not records:
            print("  <empty>")


def practice_bad_two_commits() -> None:
    print("\n=== Experiment 1: bad boundary, two commits ===")
    reset_database()

    with Session(engine) as session:
        try:
            user = User(name="Alice")
            session.add(user)
            session.commit()
            print(f"committed user first: user.id={user.id}")

            # Deliberately invalid: content is NOT NULL.
            record = LearningRecord(
                user_id=user.id,
                title="first note",
                content=None,  # type: ignore[arg-type]
            )
            session.add(record)
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            print(f"record commit failed: {exc.__class__.__name__}")

    print_database_state("after failed second commit")
    print("Question: why is Alice still in the database?")


def practice_atomic_with_flush() -> None:
    print("\n=== Experiment 2: one transaction, flush then rollback ===")
    reset_database()

    with Session(engine) as session:
        try:
            user = User(name="Bob")
            session.add(user)

            # flush sends INSERT and gives us user.id, but does not end the transaction.
            session.flush()
            print(f"flushed user, but not committed: user.id={user.id}")

            record = LearningRecord(
                user_id=user.id,
                title="first note",
                content=None,  # type: ignore[arg-type]
            )
            session.add(record)

            # commit triggers a flush for record. It will fail, then we rollback.
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            print(f"transaction failed: {exc.__class__.__name__}")

    print_database_state("after rollback")
    print("Question: why did Bob disappear even though flush inserted him?")


def practice_session_begin() -> None:
    print("\n=== Experiment 3: with session.begin() ===")
    reset_database()

    try:
        with Session(engine) as session:
            with session.begin():
                user = User(name="Carol")
                session.add(user)
                session.flush()
                print(f"inside transaction: user.id={user.id}")

                session.add(
                    LearningRecord(
                        user_id=user.id,
                        title="first note",
                        content=None,
                    )
                )
    except IntegrityError as exc:
        print(f"transaction failed: {exc.__class__.__name__}")

    print_database_state("after successful session.begin()")
    print("Question: where did commit happen?")


def main() -> None:
    practice_bad_two_commits()
    practice_atomic_with_flush()
    practice_session_begin()


if __name__ == "__main__":
    main()
