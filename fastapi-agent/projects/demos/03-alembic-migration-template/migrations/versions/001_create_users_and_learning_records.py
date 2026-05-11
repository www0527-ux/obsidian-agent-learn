"""create users and learning_records

Revision ID: 001
Revises:
Create Date: 2026-05-11
"""

from typing import Sequence, Union#sequence包含list和tuple

from alembic import op#数据结构操作工具箱
import sqlalchemy as sa#描述列、类型、约束,注意这里是as所以和之前的直接导入是一个效果


revision: str = "001"#只是示例
down_revision: Union[str, None] = None#上一个版本
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # upgrade means: move the database schema forward.
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False),
    )

    op.create_table(
        "learning_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("content", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )


def downgrade() -> None:
    # downgrade means: undo what upgrade did.
    # Drop the child table first because it depends on users.id.
    op.drop_table("learning_records")
    op.drop_table("users")
