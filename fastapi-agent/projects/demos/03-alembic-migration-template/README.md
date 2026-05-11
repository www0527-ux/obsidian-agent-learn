# 03 Alembic Migration Template

这是一个 Alembic 文件组织范本，用来学习“迁移文件应该放在哪里、每个文件负责什么、`upgrade()` / `downgrade()` 怎么读”。

这个目录先作为阅读和模仿材料，不要求立即运行。等理解结构后，再把同样思路接到真实 demo。

## 目录结构

```text
03-alembic-migration-template/
├─ app/
│  ├─ db.py
│  └─ models.py
├─ migrations/
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions/
│     ├─ 001_create_users_and_learning_records.py
│     └─ 002_add_user_email.py
├─ alembic.ini
└─ README.md
```

## 先看哪些文件

建议按这个顺序读：

1. `app/models.py`
2. `migrations/versions/001_create_users_and_learning_records.py`
3. `migrations/versions/002_add_user_email.py`
4. `migrations/env.py`
5. `alembic.ini`

## 核心关系

```text
app/models.py
  描述“当前代码希望数据库最终长什么样”

migrations/versions/*.py
  描述“数据库结构怎么一步步变化”

migrations/env.py
  把 Alembic 和 SQLAlchemy 的 Base.metadata 接起来

alembic.ini
  Alembic 命令行配置入口
```

## 最小心智模型

`create_all()` 适合从零创建 demo 数据库；Alembic 适合在已有数据的数据库上安全演进结构。

例如给 `users` 表新增 `email` 列：

```python
def upgrade() -> None:
    op.add_column("users", sa.Column("email", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "email")
```

这里 `nullable=True` 是为了照顾已有旧数据。旧的用户行没有 email，如果一开始就 `nullable=False`，数据库可能不知道旧行该填什么。

## 之后真正运行时的命令

现在不用急着运行。未来接入真实 demo 后，常见命令是：

```bash
alembic revision --autogenerate -m "add user email"
alembic upgrade head
alembic downgrade -1
```

`autogenerate` 是助手，不是裁判。它生成迁移脚本草稿后，要人工检查 `upgrade()` 和 `downgrade()`。
