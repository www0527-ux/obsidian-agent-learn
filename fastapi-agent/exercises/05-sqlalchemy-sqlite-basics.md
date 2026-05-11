# 练习：SQLAlchemy 2.0 与 SQLite 最小链路

## 目标

用一个很小的 SQLite demo 跑通 SQLAlchemy 的核心链路：

```text
engine -> model -> session -> select
```

对应 demo：

```text
projects/demos/02-sqlalchemy-sqlite-basics/
```

## 练习 1：运行最小 demo

进入 demo 目录：

```bash
cd fastapi-agent/projects/demos/02-sqlalchemy-sqlite-basics
python main.py
```

观察：

- 当前目录是否生成了 `demo.db`。
- 终端是否输出插入用户、查询用户、列出用户。

## 练习 2：解释四个核心对象

用自己的话解释：

1. `engine = create_engine("sqlite:///demo.db")` 负责什么？
2. `class User(Base)` 和数据库里的哪张表对应？
3. `with Session(engine) as session:` 代表什么？
4. `select(User).where(User.username == "alice")` 还没有执行 SQL，还是已经执行 SQL？

## 练习 3：修改 model

给 `User` 增加一个字段：

```python
display_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
```

然后修改插入逻辑，让 `alice` 有一个展示名。

思考：

- 为什么 `display_name` 可以为空？
- 如果不调用 `Base.metadata.drop_all(engine)`，已经存在的表会自动新增字段吗？

## 练习 4：增加一条查询

写一个函数：

```python
def query_user_by_email(email: str) -> User | None:
    ...
```

要求：

- 使用 `select(User).where(User.email == email)`。
- 使用 `session.scalar(stmt)`。
- 查到时打印用户信息，查不到时打印 `User not found`。

## 自测问题

1. `engine` 是一次具体数据库操作吗？
2. `session.add(user)` 之后，数据是否已经真正写进数据库？
3. `commit()` 和 `refresh()` 分别解决什么问题？
4. `select(User)` 描述的是表、Python 类，还是查询意图？
5. SQLite 适合这个阶段练习的原因是什么？

## 进阶：自己重写

如果已经理解了这个 demo，不要继续改参考答案。进入 [[06-rewrite-sqlalchemy-basics]]，从空文件重新写一遍。

## 我的答案

待补充。
