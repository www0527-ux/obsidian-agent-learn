# 练习：关系加载、预加载与 N+1

## 目标

使用 `User -> LearningRecord` 的一对多关系，观察三种查询方式的 SQL 数量和形状：

```text
lazy loading
selectinload
joinedload
```

对应文件：

```text
projects/demos/02-sqlalchemy-sqlite-basics/
```

## 文件分工

- `db.py`：`engine`、`Base`、`reset_database`
- `models.py`：`User`、`LearningRecord`、`ForeignKey`、`relationship`
- `crud.py`：创建用户、创建学习记录、基础 CRUD
- `loading_examples.py`：懒加载、`selectinload`、`joinedload` 对比
- `practice.py`：入口脚本

## 练习 1：观察懒加载

运行：

```bash
python practice.py
```

重点看 `list_users_lazy()` 对应的 SQL：

```text
1 次 SELECT users
N 次 SELECT learning_records WHERE user_id = ?
```

思考：

- 为什么循环访问 `user.records` 会触发额外 SQL？
- 如果有 100 个 user，会发多少次 records 查询？

## 练习 2：观察 selectinload

看 `list_users_with_selectinload()`：

```python
select(User).options(selectinload(User.records))
```

重点观察：

```text
SELECT users ...
SELECT learning_records ... WHERE learning_records.user_id IN (?, ?, ?)
```

思考：

- 为什么 `selectinload` 适合一对多列表？
- 它和懒加载最终拿到的数据是否相同？
- 它减少的是什么成本？

## 练习 3：观察 joinedload

看 `list_users_with_joinedload()`：

```python
select(User).options(joinedload(User.records))
```

重点观察 SQL 里是否出现 `JOIN`。

注意：

```python
session.scalars(stmt).unique().all()
```

当 `joinedload` 加载集合关系时，一条 user 可能因多条 record 在结果中重复出现，所以需要 `.unique()` 去重。

## 自测问题

1. `relationship` 是数据库列吗？
2. `ForeignKey` 和 `relationship` 分别在哪一层工作？
3. 懒加载为什么可能导致 N+1？
4. `selectinload(User.records)` 的参数为什么是 relationship 属性，而不是表名或字段名？
5. `joinedload` 加载一对多集合时为什么通常需要 `.unique()`？

