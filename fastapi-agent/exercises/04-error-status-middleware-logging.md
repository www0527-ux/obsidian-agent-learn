# 练习：错误处理、状态码、中间件与日志

## 目标

把当前 demo 从“只会成功返回”扩展成“能表达失败语义、记录请求耗时、避免泄露内部细节”的小 API。

## 练习 1：给 `/users/{user_id}` 添加 404

新增一个查询用户接口：

```python
@app.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int):
    ...
```

要求：

- 当 `user_id == 1` 时返回用户。
- 当 `user_id` 不是 1 时，抛出 `HTTPException(status_code=404, detail="User not found")`。
- 思考：为什么这里不应该返回 `{"error": "User not found"}` 加 `200`？

## 练习 2：给创建用户添加 409

在 `POST /users` 中模拟一个用户名冲突：

```text
如果 username == "alice"，表示用户名已存在，返回 409 Conflict。
```

要求：

- 使用 `HTTPException(status_code=409, detail="Username already exists")`。
- 保留 Pydantic 对 username、age、password、tags 的 422 校验。
- 思考：`409` 和 `422` 的边界是什么？

## 练习 3：添加请求耗时中间件

添加一个 middleware，给每个响应加上 `X-Process-Time` header。

要求：

- 使用 `time.perf_counter()`。
- 调用 `response = await call_next(request)`。
- 返回响应前设置 `response.headers["X-Process-Time"]`。

## 练习 4：添加基础日志

在 middleware 中记录：

```text
HTTP 方法
请求路径
响应状态码
耗时
```

要求：

- 使用 Python 标准库 `logging`。
- 不记录 password、token 等敏感信息。
- 思考：为什么日志应该记录在服务端，而不是放进响应体？

## 自测问题

1. `HTTPException` 更像是业务逻辑，还是 HTTP 层错误翻译？
2. 用户提交 JSON 字段类型不对，FastAPI 通常返回什么状态码？
3. 用户名已经存在，更适合 `400`、`409` 还是 `422`？为什么？
4. middleware 的前半段和后半段分别适合做什么？
5. 客户端看到 `request_id` 后，服务端日志为什么也要记录同一个 `request_id`？

## 我的答案

待补充。
