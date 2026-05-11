from crud import create_user, create_user_with_records, insert_record, list_records
from db import reset_database
from loading_examples import (
    list_users_lazy,
    list_users_with_joinedload,
    list_users_with_selectinload,
)


def seed_data() -> None:
    alice = create_user("alice")
    insert_record(
        alice.id,
        "学习 SQLAlchemy",
        "今天学习了 SQLAlchemy 的基本用法。",
    )

    create_user_with_records(
        "bob",
        [
            ("学习 relationship", "理解 User 和 LearningRecord 的一对多关系。"),
            ("学习懒加载", "观察访问 user.records 时 SQLAlchemy 什么时候发 SELECT。"),
        ],
    )

    create_user_with_records(
        "carol",
        [
            ("学习 selectinload", "批量加载多个用户的 records。"),
            ("学习 joinedload", "用连接方式预加载关系数据。"),
        ],
    )


if __name__ == "__main__":
    reset_database()
    seed_data()
    list_records()

    list_users_lazy()
    list_users_with_selectinload()
    list_users_with_joinedload()

