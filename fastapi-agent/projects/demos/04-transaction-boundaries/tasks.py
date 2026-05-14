from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import engine, reset_database
from models import LearningRecord, User
from practice import print_database_state


def create_user_with_default_record(name: str, title: str, content: str) -> None:
    """Task 1.

    Create a user and one default learning record as one atomic operation.

    Requirements:
    - Use one Session.
    - Use flush() to get user.id before creating the record.
    - Use exactly one final commit().
    - If anything fails, rollback and re-raise the original error.
    """
    with Session(engine) as session:
        try:
            user = User(name=name)
            session.add(user)
            session.flush()
            record=LearningRecord(
                user_id=user.id,
                title=title,
                content=content,
            )
            session.add(record)
            session.commit()
            print(f"committed user and record: user.id={user.id}, record.id={
                record.id}"
            )
        except IntegrityError:
            session.rollback()
            print("transaction failed, rolled back")
            

    # # TODO: implement this function.
    # raise NotImplementedError


def create_user_with_broken_record(name: str) -> None:
    """Task 2.

    Deliberately create a user and an invalid learning record in one transaction.

    Requirements:
    - The record must fail because content is None.
    - The user must NOT remain in the database after rollback.
    - Catch IntegrityError, rollback, print a short message, and do not re-raise.
    """
    with Session(engine) as session:
        try:
            user = User(name=name)
            session.add(user)
            session.flush()
            print(f"inside transaction: user.id={user.id}")

            session.add(
                LearningRecord(
                    user_id=user.id,
                    title="first note",
                    content=None,  # type: ignore[arg-type]
                )
            )
            session.commit()
        except IntegrityError:
            session.rollback()
            print("transaction failed, rolled back")
    # # TODO: implement this function.
    # raise NotImplementedError


def create_orphan_record() -> None:
    """Task 3.

    Try to create a LearningRecord with user_id=999 and no matching user.

    Requirements:
    - Let the database foreign key constraint fail.
    - Catch IntegrityError, rollback, print a short message, and do not re-raise.
    - The database must remain empty afterward.
    """
    with Session(engine) as session:
        try:
            with session.begin():
                session.add(
                    LearningRecord(
                        user_id=999,
                        title="orphan note",
                        content="this record has no valid user",
                    )
                )
        except IntegrityError:
            session.rollback()#可以不要，因为session.begin()会在异常时自动回滚，但加上也没问题
            print("failed to create orphan record, rolled back")
        
    # # TODO: implement this function.
    # raise NotImplementedError


def main() -> None:
    reset_database()
    create_user_with_default_record("Dora", "first note", "hello transaction")
    print_database_state("after task 1")

    reset_database()
    create_user_with_broken_record("Eve")
    print_database_state("after task 2")

    reset_database()
    create_orphan_record()
    print_database_state("after task 3")


if __name__ == "__main__":
    main()
