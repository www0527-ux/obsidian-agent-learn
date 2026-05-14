# Exercises

## 1. 先观察

运行：

```bash
python practice.py
```

回答：

```text
Experiment 1 为什么留下了 Alice？
Experiment 2 为什么 Bob 消失了？
Experiment 3 的 commit 发生在代码的哪一行附近？
```

## 2. 改出一个失败的 session.begin()

在 `practice_session_begin()` 里，把 record 的 `content` 改成 `None`：

```python
content=None
```

再运行：

```bash
python practice.py
```

观察：

```text
Carol 有没有留在 users 表？
为什么？
```

## 3. 自己新增一个练习函数

新增函数：

```python
def practice_foreign_key_failure() -> None:
    ...
```

目标：

```text
不要创建 user，直接创建 user_id=999 的 LearningRecord。
让数据库触发外键失败。
捕获 IntegrityError，rollback。
最后打印数据库状态，确认没有留下记录。
```

提示：

```python
record = LearningRecord(
    user_id=999,
    title="orphan record",
    content="should fail",
)
```

## 4. 写一句总结

用自己的话写：

```text
flush 不破坏原子性，因为：
提前 commit 会破坏原子性，因为：
```

## 5. 实践任务

打开 `tasks.py`，补完三个函数：

```text
create_user_with_default_record()
create_user_with_broken_record()
create_orphan_record()
```

然后运行：

```bash
python check_tasks.py
```

目标输出：

```text
PASS check_task_1
PASS check_task_2
PASS check_task_3
```
