# 07 表关系、懒加载/预加载与 N+1

## Core Idea

SQLAlchemy 的 `relationship` 让 ORM 对象之间可以互相导航，例如 `user.records` 和 `record.user`。加载这些关系时，lazy loading、`selectinload`、`joinedload` 的差异不只是 SQL 写法不同，也会影响 ORM 如何把 SQL 行还原成 Python 对象。

这一节的核心心智模型：

```text
SQL 行 -> identity map 识别对象身份 -> relationship loader 填充关系集合 -> Result 返回对象
```

## joinedload 与 unique 的底层过程

当使用：

```python
stmt = select(User).options(joinedload(User.records))
users = session.scalars(stmt).unique().all()
```

`joinedload(User.records)` 会用 JOIN 风格把 `users` 和 `learning_records` 放进同一次查询。假设一个用户有两条记录，底层 SQL 行会类似：

```text
users.id | users.name | records.id | records.title
1        | Alice      | 10         | SQLAlchemy CRUD
1        | Alice      | 11         | Relationship Loading
```

从 SQL 角度看，这两行不是重复行，因为 record 不同。但从 `select(User)` 的角度看，它们都对应同一个父对象：

```text
User + primary_key=(1,)
```

SQLAlchemy 处理这些行时，不是先创建两个独立的 `User(id=1)`，再由 `unique()` 合并它们。更准确的过程是：

```text
第 1 行：
  identity map 发现/创建 User(id=1)
  relationship loader 把 Record(id=10) 加入 User(id=1).records

第 2 行：
  identity map 发现这还是 User(id=1)，复用同一个 Python 对象
  relationship loader 把 Record(id=11) 加入同一个 User(id=1).records

最后：
  unique() 过滤 Result 里重复出现的 User 引用
```

所以在 `unique()` 之前，逻辑上的结果流可能像：

```python
[
    same_user,
    same_user,
]
```

这两个位置指向的是同一个 Python 对象，而不是两个各自只带一条 record 的对象。此时 `same_user.records` 已经包含多条记录：

```python
same_user.records == [
    LearningRecord(id=10),
    LearningRecord(id=11),
]
```

`unique()` 做的是最终结果流去重：

```python
[
    same_user,
    same_user,
]
```

变成：

```python
[
    same_user,
]
```

它不会丢掉 `records`，因为 `records` 的装配已经由 ORM 的 relationship loader 完成。

## unique 的去重标准

在 ORM 场景里，`unique()` 主要依据 ORM 实体身份去重：

```text
实体类型 + 主键值
```

例如：

```text
(User, 1)
(User, 2)
```

它不是 SQL 的 `DISTINCT`，也不是比较整行 SQL 是否完全一样。对 `joinedload(User.records)` 这种集合预加载来说，SQL 行必须展开成多行，ORM 才能看到每一条子记录；`unique()` 只是避免最后把同一个父对象重复返回。

## scalars、execute 与 unique 的关系

`session.scalars(stmt)` 基本可以理解为：

```python
session.execute(stmt).scalars()
```

对于：

```python
select(User).options(joinedload(User.records))
```

`execute()` 的逻辑结果是 row：

```python
(User(id=1),)
(User(id=1),)
```

`scalars()` 取每个 row 的第一个元素，所以得到的是：

```python
User(id=1)
User(id=1)
```

这时调用：

```python
session.scalars(stmt).unique().all()
```

就是对 `User` 结果流去重。

也可以写成：

```python
session.execute(stmt).unique().scalars().all()
```

但在 `select(User)` 这个场景里，`session.scalars(stmt).unique().all()` 更直接表达意图：我要的是去重后的 `User` 列表。

## Key Points

- `joinedload` 加载一对多集合时，父对象会因为多条子记录在 SQL 结果中展开成多行。
- 展开的多行不代表 ORM 会创建多个独立父对象；identity map 会按实体类型和主键复用同一个 Python 对象。
- relationship loader 负责把每一行里的子对象填进同一个父对象的集合属性。
- `unique()` 负责过滤最终结果流中重复出现的父对象引用。
- `unique()` 不会丢失已经装配进 `user.records` 的子对象。
- `unique()` 不是 SQL `DISTINCT`；它是 Python/ORM 结果层面的去重。

## My Understanding

重复的 SQL 行都指向同一个 `User`；每行贡献一个 `LearningRecord` 给这个 `User.records`；`unique()` 再把结果流里重复出现的同一个 `User` 引用过滤掉。

相关：[[06-sqlalchemy-core-concepts]]
