# 3.1 FastAPI 分层结构：router、service、repository、schema、model

## Core Idea
FastAPI 应用分层的目的不是把文件拆得更多，而是让每一层只承担一种变化原因。router 负责 HTTP 边界，schema 负责输入输出契约，service 负责业务规则，repository 负责数据库访问，model 负责数据库结构与 ORM 映射。

## Layer Map
- `router`: 接收请求、声明路径/状态码/依赖、把业务异常转换成 HTTP 响应。
- `schema`: 定义 API 输入输出的 Pydantic 模型，是外部世界看到的数据契约。
- `service`: 编排业务流程和规则，例如创建用户、处理冲突、调用多个 repository。
- `repository`: 封装具体查询和持久化语句，让 service 不直接散落 SQLAlchemy 查询细节。
- `model`: SQLAlchemy ORM 模型，表达表结构、字段、关系和约束。

## Mental Boundary
一条常用判断：如果代码在乎 `status_code`、`Depends`、`HTTPException`，它多半属于 router；如果代码在乎业务含义和失败规则，它多半属于 service；如果代码在乎 `select()`、`add()`、`commit()`、`refresh()`，它多半属于 repository 或数据库边界。

## Example From Current Demo
- `app/api/users.py`: router 层，暴露 `POST /users`，把 `UserNameConflictError` 转成 `409 Conflict`。
- `app/services/users.py`: service 层，当前同时承担了业务规则和数据库写入。
- `app/schemas.py`: schema 层，定义 `UserCreate` 与 `UserRead`。
- `app/models.py`: model 层，定义 `User` 和 `LearningRecord`。
- `app/db.py`: 数据库基础设施，提供 `AsyncSession` 和建表逻辑。

## Design Heuristic
小 demo 可以让 service 直接使用 session；当查询变复杂、多个业务流程复用同一组查询、或需要更容易测试时，再拆出 repository。

## Connections
- Related to: [[06-sqlalchemy-core-concepts]]
- Related to: [[07-relationships-loading-n-plus-one]]
- Prerequisite for: [[09-dependency-injection-session-service]]

## My Understanding
待补充：用自己的话解释一次 router、service、repository、schema、model 的边界。
