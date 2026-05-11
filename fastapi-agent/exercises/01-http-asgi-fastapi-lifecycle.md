# 练习 01：最小 FastAPI 请求生命周期

## 目标

用一个最小 demo 建立请求生命周期的直觉。

## 任务

- 创建一个 FastAPI app，包含 `GET /health` 和 `POST /echo`。
- `POST /echo` 接收 JSON：`{"message": "hello"}`。
- 返回 JSON：`{"received": "hello", "length": 5}`。
- 故意传错字段名，观察 FastAPI 返回的验证错误。
- 写 5 句话说明这次请求分别经过了哪些环节。

## 复盘问题

- FastAPI 为什么能自动知道请求体字段错了？
- endpoint 返回 Python 字典后，什么时候变成 JSON？
- 如果 `/echo` 内部抛异常，应该在哪一层处理更合适？

