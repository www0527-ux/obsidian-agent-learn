# 3.1 分层结构：router、service、repository、schema、model

## Core Idea
分层结构把一次请求拆成清晰的责任链：router 处理 HTTP 输入输出和状态码，service 编排业务规则并暴露业务异常，repository 封装数据库读写，schema 定义 API 契约，model 映射数据库表。这样错误边界和业务边界不会混在同一个函数里。

## Key Points
- router 不直接写数据库规则，主要负责 Depends、response_model、HTTPException 和状态码。
- service 拥有业务事务边界，并把 IntegrityError 等底层异常翻译成业务异常。
- repository 负责 select、add、flush 等持久化细节，但不决定 HTTP 响应。
- 真实请求验证 201、409、404 是确认分层是否落地的重要方式。

## Examples
- POST /users 第一次创建 alice 返回 201。
- POST /users 重复 alice 时，数据库唯一约束冲突经 service 转成 UserNameConflictError，再由 router 转成 409。
- GET /users/999 查不到用户时，service 抛 UserNotFoundError，router 转成 404。

## Connections
- Related to: [[2.3 不遮蔽数据库细节的 CRUD 写法]]
- Related to: [[2.6 事务、并发与失败边界]]
- Prerequisite for: [[3.2 用依赖注入管理数据库 session 和业务服务]]
- Prerequisite for: [[3.4 FastAPI 测试：单元测试、集成测试、测试数据库]]

## My Understanding
请用自己的话补充：一次 POST /users 请求从 router 到 service、repository、model、schema 是如何流动的？
