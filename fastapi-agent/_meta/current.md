# Current Learning State: fastapi + agent

## Now
- Topic: FastAPI + Agent
- Module: 模块 2：数据库与 SQLAlchemy
- Current concept: 2.5 Alembic 迁移与数据库结构演进
- Last session: 2026-05-11
- Learner level: intermediate
- Next action: 阅读 `projects/demos/03-alembic-migration-template/` 范本，先理解 `models.py`、`migrations/env.py`、`versions/*.py` 的分工，再模仿写一个迁移。

## Mastered
- 2.3 不遮蔽数据库细节的 CRUD 写法
- 2.4 表关系、懒加载/预加载与 N+1 问题

## Current Notes
- 已记录：`joinedload` 加载集合关系时，SQL 行会展开；identity map 复用同一个父对象；relationship loader 填充 `records`；`unique()` 只过滤最终结果流里的重复父对象引用，不会丢失子对象。
- 2.4 收尾自测通过：能解释 `selectinload` 两次查询与外键归档、`relationship` append/flush 同步时机，以及三种加载策略的 SQL 次数。小纠正：100 个 user 的 lazy loading 是 1 + 100 = 101 次 SQL，不是 301 次；300 更接近 records 结果行数量。
- 2.5 已新增 Alembic 文件组织范本：`projects/demos/03-alembic-migration-template/`。当前目标是先读懂文件分工，不急着运行。

## Due Review
- 2.3 不遮蔽数据库细节的 CRUD 写法 (due: 2026-05-12)
- 2.4 表关系、懒加载/预加载与 N+1 问题 (due: 2026-05-12)

## Read Next
- exercises/07-relationships-loading-n-plus-one.md
- notes/07-relationships-loading-n-plus-one.md
- projects/demos/03-alembic-migration-template/README.md
- projects/demos/03-alembic-migration-template/migrations/versions/001_create_users_and_learning_records.py
- projects/demos/03-alembic-migration-template/migrations/versions/002_add_user_email.py
- projects/roadmap.md

## Resume Rule
- Start here before reading the long progress log.
- Read `_meta/progress.md` only when historical detail is requested.
