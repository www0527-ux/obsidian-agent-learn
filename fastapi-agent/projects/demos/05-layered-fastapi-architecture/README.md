# 05 Layered FastAPI Architecture Practice

目标：练习 FastAPI 应用分层，并用自己的话解释每个文件的职责和关系。

## Suggested Flow
1. 先阅读目录结构。
2. 补全每个文件中的 TODO。
3. 解释一次请求从 `router` 到 `service`、`repository`、`model`、`schema` 的流动。
4. 标出你觉得“也可以放在别处”的责任，并说明取舍。

## Layers
- `app/main.py`: 创建 FastAPI app，挂载 router，注册全局异常处理。
- `app/api/routes/users.py`: HTTP 入口，只处理请求/响应/状态码/依赖。
- `app/api/deps.py`: FastAPI 依赖装配层，例如 session、service。
- `app/schemas/users.py`: API 输入输出契约。
- `app/models/users.py`: SQLAlchemy ORM 模型。
- `app/repositories/users.py`: 数据库查询和持久化细节。
- `app/services/users.py`: 业务规则和业务异常。
- `app/core/exceptions.py`: 业务异常类型。
- `app/db/session.py`: 数据库 engine/session 基础设施。

## Practice Question
当“用户名重复”发生时，你希望异常沿着哪条路径传播？

```text
database -> repository -> service -> router/handler -> HTTP response
```

写下你自己的版本。
