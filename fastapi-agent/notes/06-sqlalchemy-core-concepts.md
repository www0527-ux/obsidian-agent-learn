# 06 SQLAlchemy 2.0 核心概念

## Core Idea

SQLAlchemy 不是数据库，也不是一门新语言，而是 Python 里的数据库工具库/ORM。它把 Python 类、Python 对象和查询表达式，连接到 SQLite、PostgreSQL、MySQL 等真实数据库。

这一节的核心链路：

```text
engine -> Base/model -> metadata/create_all -> Session -> add/commit/refresh -> select/scalar/scalars
```

## SQLite、SQLAlchemy 与连接配置

SQLite 是轻量嵌入式关系型数据库。它不需要单独启动数据库服务，通常就是一个本地数据库文件，例如：

```text
practice.db
demo.db
```

SQLAlchemy 是 Python 访问数据库的工具层。它负责把 Python 里的 ORM model、对象状态、查询表达式转换成数据库能执行的 SQL。

数据库连接配置集中体现在：

```python
engine = create_engine("sqlite:///practice.db", echo=True)
```

含义：

```text
sqlite              使用 SQLite
:///practice.db     使用当前目录下的 practice.db 文件
echo=True           把实际执行的 SQL 打印出来，便于学习和调试
```

后续真实项目里不应把连接字符串写死，而应放到 settings：

```python
engine = create_engine(settings.database_url)
```

相关：[[05-configuration-environment-settings]]

## Base 与 metadata

SQLAlchemy 2.0 声明式 ORM 通常先定义一个基类：

```python
class Base(DeclarativeBase):
    pass
```

这个 `Base` 是当前项目的 ORM model 基类。所有继承它的类都会被 SQLAlchemy 识别为 ORM model：

```python
class LearningRecord(Base):
    __tablename__ = "learning_records"
```

`Base.metadata` 可以理解成“表结构说明书集合”。它收集所有继承 `Base` 的 model 对应的表、列、主键、约束等信息。

```python
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
```

含义：

```text
drop_all(engine)     根据 metadata 删除数据库中对应的表
create_all(engine)   根据 metadata 创建数据库中还不存在的表
```

这适合练习、测试和 demo。生产环境不能随便 `drop_all`，因为它会删表和数据；真实项目通常用 Alembic migration 演进表结构。

## mapped_column、Column 与 Mapped

传统写法常见：

```python
id = Column(Integer, primary_key=True)
```

SQLAlchemy 2.0 更推荐类型标注友好的写法：

```python
id: Mapped[int] = mapped_column(primary_key=True)
title: Mapped[str] = mapped_column(String(100), nullable=False)
```

`Mapped[str]` 的含义是：

```text
这是 SQLAlchemy ORM 管理的映射属性；
在 Python 里读出来时，它表现为 str 类型。
```

不要简单写成：

```python
title: str = mapped_column(...)
```

因为它不是普通字符串属性，而是 ORM 管理的映射字段。

`mapped_column(...)` 描述数据库列如何生成，例如类型、主键、是否可空、是否唯一。

## 默认当前时间

练习中写法：

```python
created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.utcnow,
    nullable=False,
)
```

注意传的是函数本身：

```python
default=datetime.utcnow
```

而不是：

```python
default=datetime.utcnow()
```

区别：

```text
datetime.utcnow      每次插入时调用，生成当时的时间
datetime.utcnow()    类定义时立刻调用，容易让多条记录复用同一个时间
```

## ORM 对象生命周期

这句之后：

```python
record = LearningRecord(title=title, content=content)
```

`record` 已经是 ORM 对象，因为 `LearningRecord` 本身是 ORM model class。

但它还没有被 session 管理，也还没有写入数据库。

生命周期可以这样理解：

```text
record = LearningRecord(...)   transient，临时态，普通内存对象
session.add(record)            pending，交给 session 管理，等待写入
session.commit()               flush + commit，发 INSERT 并提交事务
session.refresh(record)        从数据库重新加载生成后的字段
with Session(...) 结束          detached，脱离 session，但对象仍在内存中
```

关键区分：

```text
是不是 ORM 对象：由类决定，实例化后就是
是否被 session 管理：由 session.add 决定
是否写进数据库：由 flush/commit 决定
```

## session.add、flush、commit

`session.add(record)` 的直接含义不是“立刻 INSERT”，而是：

```text
请 session 开始追踪这个 ORM 对象
```

如果对象是新对象，那么后续 `flush()` 或 `commit()` 时，SQLAlchemy 会为它生成 `INSERT`。

```text
add       不发 SQL，只把对象纳入 session 管理
flush     发 SQL，例如 INSERT/UPDATE，但不一定提交事务
commit    先 flush，再提交事务
```

如果在 `add` 后、第一次 `commit` 前修改对象：

```python
record = LearningRecord(title="旧标题", content="旧内容")
session.add(record)
record.title = "新标题"
session.commit()
```

通常只会发一条 `INSERT`，并且插入的是“新标题”。不会先 `INSERT` 旧标题，再 `UPDATE` 新标题。

如果已经 commit 过，再修改：

```python
session.commit()       # INSERT
record.title = "新标题"
session.commit()       # UPDATE
```

第二次提交会发 `UPDATE`。

## commit 后对象还能不能用

`commit()` 后，`record` 这个 Python 对象还存在，也通常还能读已经加载过的属性。

但 `with Session(...)` 结束后，session 关闭，`record` 会变成 detached。detached 对象不是不能用；只是如果某个属性需要回数据库懒加载或重新加载，就可能出问题。

更稳的项目习惯：

```text
在 session 内查/改 ORM 对象
commit/refresh
转换成 Pydantic response schema 或普通数据结构
再返回到 API 边界外
```

## select、execute、scalar、scalars

先假设表里有两条记录：

```text
id | title
1  | SQLAlchemy
2  | FastAPI
```

查询语句：

```python
stmt = select(LearningRecord)
```

### execute

```python
rows = session.execute(stmt).all()
```

得到的是“行”结果，形状大概像：

```text
[
  (record1,),
  (record2,),
]
```

也就是每行外面还有一层容器。

### scalars

```python
records = session.scalars(stmt).all()
```

得到的是 ORM 对象列表：

```text
[
  record1,
  record2,
]
```

对于 `select(LearningRecord)`，更常用 `scalars()`，因为我们想要的通常就是 `LearningRecord` 对象本身。

### scalar

```python
record = session.scalar(stmt)
```

得到第一行的第一个值：

```text
record1
```

如果没有结果，返回 `None`。如果有多条结果，`scalar()` 不会自动帮你报错，它只是取第一条。

### 更严格的一条查询

如果业务语义要求“最多一条”：

```python
record = session.scalar_one_or_none(stmt)
```

如果业务语义要求“必须正好一条”：

```python
record = session.scalar_one(stmt)
```

简化记忆：

```text
execute(stmt).all()     -> [(record1,), (record2,)]
scalars(stmt).all()     -> [record1, record2]
scalar(stmt)            -> record1 或 None
scalar_one_or_none()    -> 0 或 1 条，多条报错
scalar_one()            -> 必须正好 1 条，否则报错
```

## 当前练习代码心智模型

```python
def query_record_by_title(title: str) -> LearningRecord | None:
    with Session(engine) as session:
        stmt = select(LearningRecord).where(LearningRecord.title == title)
        record = session.scalar(stmt)
        return record
```

拆开看：

```text
select(LearningRecord)                 查询 LearningRecord ORM 对象
.where(LearningRecord.title == title)  添加过滤条件
session.scalar(stmt)                   执行查询，取第一行第一列
```

如果 `title` 不是唯一字段，`scalar()` 只取第一条。若希望标题唯一，要么给 `title` 加 `unique=True`，要么使用更严格的 `scalar_one_or_none()` 来暴露重复数据问题。

## My Understanding

待补充：用自己的话解释 `engine`、`Base.metadata`、`Session`、`add/commit/refresh` 和 `scalar/scalars` 的区别。

