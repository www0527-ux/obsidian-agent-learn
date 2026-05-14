from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

import tasks
from db import engine, reset_database
from models import LearningRecord, User


def count_rows() -> tuple[int, int]:
    with Session(engine) as session:
        user_count = len(list(session.scalars(select(User))))
        record_count = len(list(session.scalars(select(LearningRecord))))
        return user_count, record_count


def check_task_1() -> None:
    reset_database()
    tasks.create_user_with_default_record("Dora", "first note", "hello transaction")

    with Session(engine) as session:
        users = list(session.scalars(select(User)))
        records = list(session.scalars(select(LearningRecord)))

    assert len(users) == 1, f"expected 1 user, got {len(users)}"
    assert len(records) == 1, f"expected 1 record, got {len(records)}"
    assert records[0].user_id == users[0].id, "record.user_id should point to the created user"


def check_task_2() -> None:
    reset_database()
    tasks.create_user_with_broken_record("Eve")
    assert count_rows() == (0, 0), "broken record should rollback the user too"


def check_task_3() -> None:
    reset_database()
    tasks.create_orphan_record()
    assert count_rows() == (0, 0), "orphan record should not remain in the database"


def main() -> None:
    checks = [check_task_1, check_task_2, check_task_3]
    for check in checks:
        check()
        print(f"PASS {check.__name__}")


if __name__ == "__main__":
    main()
