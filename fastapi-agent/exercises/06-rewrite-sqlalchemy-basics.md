# 练习：从零重写 SQLAlchemy 最小链路

## 目标

不要复制 `02-sqlalchemy-sqlite-basics/main.py`。新建一个空文件，自己重新写一遍最小链路：

```text
engine -> Base -> model -> create_all -> Session -> add -> commit -> select
```

建议新建：

```text
projects/demos/02-sqlalchemy-sqlite-basics/practice.py
```

## 练习 1：只创建数据库和表

要求：

- 创建 `engine`，连接到 `practice.db`。
- 定义 `Base`。
- 定义 `LearningRecord` model，对应表名 `learning_records`。
- 字段：
  - `id`：主键
  - `title`：字符串，非空
  - `content`：字符串，非空
  - `created_at`：时间，默认当前时间，非空
- 写一个 `reset_database()`：
  - 先 `drop_all`
  - 再 `create_all`

完成后运行文件，确认目录里出现 `practice.db`。

## 练习 2：插入一条学习记录

写函数：

```python
def insert_record() -> LearningRecord:
    ...
```

要求：

- 使用 `with Session(engine) as session:`。
- 创建一条 `LearningRecord`。
- 调用 `session.add(record)`。
- 调用 `session.commit()`。
- 调用 `session.refresh(record)`。
- 打印新记录的 `id` 和 `title`。

思考：

- 如果没有 `commit()`，数据库文件里会真的保存这条记录吗？
- 如果没有 `refresh()`，为什么有时拿不到数据库生成后的字段？

## 练习 3：按标题查询

写函数：

```python
def query_record_by_title(title: str) -> LearningRecord | None:
    ...
```

要求：

- 使用 `select(LearningRecord).where(LearningRecord.title == title)`。
- 使用 `session.scalar(stmt)`。
- 查到时打印 `id/title/content`。
- 查不到时打印 `Record not found`。

## 练习 4：列出全部记录

写函数：

```python
def list_records() -> list[LearningRecord]:
    ...
```

要求：

- 使用 `session.scalars(select(LearningRecord).order_by(LearningRecord.id))`。
- 打印每一条记录。
- 返回记录列表。

## 练习 5：故意触发一次唯一约束错误

把 `title` 改成唯一：

```python
title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
```

连续插入两条相同 title 的记录，观察报错。

思考：

- 这个错误发生在 `add()` 时，还是 `commit()` 时？
- 为什么唯一约束应该由数据库兜底，而不是只靠 Python 代码提前判断？

## 自测问题

1. `Base.metadata` 里保存了什么信息？
2. `drop_all(engine)` 会删除什么？
3. `create_all(engine)` 会创建什么？
4. 为什么练习 demo 可以用 `drop_all`，真实生产环境不能随便用？
5. `select(...)` 和 `session.scalar(...)` 分别负责什么？

