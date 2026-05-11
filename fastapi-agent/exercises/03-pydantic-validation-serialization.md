# 练习 03：Pydantic 校验、序列化与响应模型

## 目标

通过一个小接口练习 Pydantic 的字段约束、自定义校验、响应过滤和 422 错误观察。

## 任务

在 `projects/demos/01-minimal-fastapi-api/app/main.py` 里新增一个接口：

```text
POST /users
```

请求体模型 `UserCreate`：

- `username`: 字符串，长度 3-20，不能包含空格。
- `age`: 整数，范围 0-150。
- `password`: 字符串，长度至少 8。
- `tags`: 字符串列表，默认空列表，最多 5 个。

响应模型 `UserRead`：

- `id`: int
- `username`: str
- `age`: int
- `tags`: list[str]

要求：

- endpoint 内部可以假装创建用户，直接返回一个字典。
- 返回字典里故意包含 `password` 或 `password_hash`。
- 使用 `response_model=UserRead` 确认密码相关字段不会返回给客户端。
- 用 `/docs` 分别测试合法请求和非法请求。

## 推荐观察

测试这些非法请求：

1. `username` 少于 3 个字符。
2. `username` 包含空格。
3. `age` 是负数。
4. `password` 少于 8 个字符。
5. `tags` 超过 5 个。

每次观察 422 响应里的：

- `loc`
- `type`
- `msg`

## 复盘问题

1. 哪些校验可以用 `Field()` 表达？
2. 哪些校验需要用 `field_validator()`？
3. `response_model` 为什么能过滤掉 `password_hash`？
4. 为什么请求模型和响应模型不要混用？

