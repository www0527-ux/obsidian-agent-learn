# 04 Transaction Boundaries

这个 demo 用来练习 SQLAlchemy 里的事务边界：

```text
add      -> 把对象交给 Session 管理
flush    -> 发 SQL，但事务还没有结束
commit   -> 提交事务，结果正式保存
rollback -> 回滚当前事务里未提交的改动
```

## 运行

从这个目录执行：

```bash
python practice.py
```

每个实验都会重置本地 SQLite 数据库 `transaction_practice.db`。

## 练习目标

1. 观察提前 `commit()` 为什么会留下半完成状态。
2. 观察 `flush()` 可以拿到 `user.id`，但失败后仍然能整体回滚。
3. 观察 `with session.begin()` 如何自动管理 commit/rollback。

## 你要重点看

- `practice_bad_two_commits()`
- `practice_atomic_with_flush()`
- `practice_session_begin()`

读代码时问自己：

```text
这次业务操作的成功/失败边界是什么？
中间有没有提前 commit？
异常发生后，数据库会留下什么？
```
