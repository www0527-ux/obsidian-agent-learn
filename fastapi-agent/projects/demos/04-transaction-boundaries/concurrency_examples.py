from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import engine, reset_database
from models import LearningRecord, User


def seed_record() -> int:
    reset_database()

    with Session(engine) as session:
        user = User(name="Alice")
        session.add(user)
        session.flush()

        record = LearningRecord(
            user_id=user.id,
            title="concurrency note",
            content="watch the counter",
        )
        session.add(record)
        session.commit()
        return record.id


def print_record(label: str, record_id: int) -> None:
    with Session(engine) as session:
        record = session.get(LearningRecord, record_id)
        if record is None:
            print(f"{label}: <missing>")
            return

        print(
            f"{label}: id={record.id}, title={record.title}, "
            f"view_count={record.view_count}"
        )


def demonstrate_lost_update() -> None:
    print("\n=== Experiment 1: lost update ===")
    record_id = seed_record()
    print_record("initial", record_id)

    session_a = Session(engine)
    session_b = Session(engine)
    try:
        record_a = session_a.get(LearningRecord, record_id)
        record_b = session_b.get(LearningRecord, record_id)

        assert record_a is not None
        assert record_b is not None#断言

        print(f"session A reads view_count={record_a.view_count}")
        print(f"session B reads view_count={record_b.view_count}")

        record_a.view_count += 1
        session_a.commit()
        print("session A commits +1")
        #虽然提交有先后，但是session B 仍然基于旧值进行更新，导致 session A 的更新被覆盖了。
        record_b.view_count += 1
        session_b.commit()
        print("session B commits +1 based on its old value")
    finally:
        session_a.close()
        session_b.close()

    print_record("final", record_id)
    print("Expected by business: 2. Actual result shows whether one update was lost.")


def demonstrate_atomic_update() -> None:
    print("\n=== Experiment 2: atomic database UPDATE ===")
    record_id = seed_record()
    print_record("initial", record_id)

    session_a = Session(engine)
    session_b = Session(engine)
    try:
        stmt = (
            update(LearningRecord)
            .where(LearningRecord.id == record_id)
            .values(view_count=LearningRecord.view_count + 1)
        )

        session_a.execute(stmt)
        session_a.commit()
        print("session A commits database-side +1")

        session_b.execute(stmt)
        session_b.commit()
        print("session B commits database-side +1")
    finally:
        session_a.close()
        session_b.close()

    print_record("final", record_id)
    print("Because the +1 happened inside UPDATE, both increments are preserved.")


def demonstrate_unique_constraint_conflict() -> None:
    print("\n=== Experiment 3: unique constraint conflict ===")
    reset_database()

    session_a = Session(engine)
    session_b = Session(engine)
    try:
        session_a.add(User(name="alice"))
        session_b.add(User(name="alice"))

        session_a.commit()
        print("session A commits user name='alice'")

        try:
            session_b.commit()
        except IntegrityError as exc:
            session_b.rollback()
            print(f"session B failed: {exc.__class__.__name__}")
            print("API translation idea: IntegrityError -> HTTP 409 Conflict")
    finally:
        session_a.close()
        session_b.close()

    with Session(engine) as session:
        users = list(session.scalars(select(User).order_by(User.id)))
        print("users after conflict:")
        for user in users:
            print(f"  id={user.id}, name={user.name}")


def main() -> None:
    demonstrate_lost_update()
    demonstrate_atomic_update()
    demonstrate_unique_constraint_conflict()


if __name__ == "__main__":
    main()
