from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine
from models import LearningRecord, User


def create_user(name: str) -> User:
    with Session(engine) as session:
        user = User(name=name)
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"Created user: id={user.id}, name={user.name}")
        return user


def insert_record(user_id: int, title: str, content: str) -> LearningRecord | None:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            print(f"No user found with id: {user_id}")
            return None

        record = LearningRecord(user_id=user_id, title=title, content=content)
        session.add(record)
        session.commit()
        session.refresh(record)
        print(f"Inserted record: id={record.id}, user_id={record.user_id}, title={record.title}")
        return record


def create_user_with_records(name: str, records_data: list[tuple[str, str]]) -> User:
    with Session(engine) as session:
        user = User(name=name)
        for title, content in records_data:
            user.records.append(LearningRecord(title=title, content=content))

        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"Created user with records: id={user.id}, name={user.name}")
        return user


def query_record_by_title(title: str) -> LearningRecord | None:
    with Session(engine) as session:
        stmt = select(LearningRecord).where(LearningRecord.title == title)
        record = session.scalar(stmt)
        if record is None:
            print(f"No record found with title: {title}")
            return None
        print(f"Queried record: id={record.id}, title={record.title}, content={record.content}")
        return record


def list_records() -> list[LearningRecord]:
    with Session(engine) as session:
        stmt = select(LearningRecord).order_by(LearningRecord.id)
        records = list(session.scalars(stmt).all())
        print("All records:")
        for record in records:
            print(f"- id={record.id}, user_id={record.user_id}, title={record.title}")
        return records


def get_record(record_id: int) -> LearningRecord | None:
    with Session(engine) as session:
        stmt = select(LearningRecord).where(LearningRecord.id == record_id)
        record = session.execute(stmt).scalar_one_or_none()
        if record is None:
            print(f"No record found with id: {record_id}")
            return None
        print(f"Queried record: id={record.id}, title={record.title}, content={record.content}")
        return record


def update_record(record_id: int, new_title: str, new_content: str) -> LearningRecord | None:
    with Session(engine) as session:
        record = session.get(LearningRecord, record_id)
        if record is None:
            print(f"No record found with id: {record_id}")
            return None

        record.title = new_title
        record.content = new_content
        session.commit()
        session.refresh(record)
        print(f"Updated record: id={record.id}, title={record.title}, content={record.content}")
        return record


def delete_record(record_id: int) -> bool:
    with Session(engine) as session:
        record = session.get(LearningRecord, record_id)
        if record is None:
            print(f"No record found with id: {record_id}")
            return False

        session.delete(record)
        session.commit()
        print(f"Deleted record with id: {record_id}")
        return True

