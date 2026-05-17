# Session 47 - 2026-05-14

- Module: 模块 3：FastAPI 应用架构
- Concept: 3.1 分层结构：router、service、repository、schema、model

## Summary
完成 05-layered-fastapi-architecture demo 的分层架构实践：schemas 定义输入输出模型，repository 封装查询与持久化，service 编排创建/查询用户并把完整性约束冲突转换成 UserNameConflictError，router 捕获业务错误和 SQLAlchemyError 并转换成对应 HTTP 响应。

## Covered Concepts
- 3.1 分层结构：router、service、repository、schema、model
- 业务异常与 HTTP 异常的边界
- IntegrityError 到业务错误的转换
- SQLAlchemyError 向上抛出并由 router 转换为 HTTP 500

## Mastered Concepts
- None

## Wins
- 能区分业务异常和基础设施异常
- 把唯一性约束冲突从 IntegrityError 转换成更具体的业务错误
- 让 router 统一承担 HTTPException/status_code/detail 的转换职责

## Struggles
- 还需要通过请求或测试验证 404、409、500 路径
- 代码中仍有少量 TODO、格式和重复构造异常对象的小问题

## Next Session
用几个最小测试或 curl/httpx 请求验证 POST /users 重名返回 409、GET /users/{id} 不存在返回 404，并清理异常处理代码中的小重复；通过验证后再把 3.1 标记为掌握。
