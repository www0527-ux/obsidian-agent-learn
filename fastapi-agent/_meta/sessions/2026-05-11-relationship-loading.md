# Session Detail - 2026-05-11 Relationship Loading

## Summary
进入 2.4 表关系、懒加载/预加载与 N+1 问题。已经把 SQLAlchemy 练习代码拆分为 `db.py`、`models.py`、`crud.py`、`loading_examples.py` 和入口 `practice.py`，并验证了 lazy loading、`selectinload`、`joinedload` 三种关系加载方式。

## Key Observations
- `ForeignKey` 是数据库列约束，`relationship` 是 ORM 层对象导航属性。
- `back_populates` 声明双向关系，让 `user.records` 和 `record.user` 彼此对应。
- 懒加载在循环访问 `user.records` 时会按用户逐次发出查询，形成 N+1 查询形态。
- `selectinload(User.records)` 会先查用户，再用 `WHERE user_id IN (...)` 批量加载记录。
- `joinedload(User.records)` 会用 JOIN 风格预加载集合关系，结果需要 `.unique()` 去重父对象。
- 对 `joinedload` + `.unique()` 的底层过程形成更准确理解：SQL 行会因一对多集合展开；identity map 按实体类型和主键复用同一个 `User`；relationship loader 把每一行里的 `LearningRecord` 填进同一个 `User.records`；`.unique()` 只过滤最终结果流里重复出现的父对象引用，不负责合并两个独立 `User`，也不会丢失已装配的 `records`。
- 已新增笔记：[[../../notes/07-relationships-loading-n-plus-one]]。

## Next Session
重点练习 `selectinload(User.records)` 的参数含义，并对比 `selectinload` 与 `joinedload` 的适用场景。
