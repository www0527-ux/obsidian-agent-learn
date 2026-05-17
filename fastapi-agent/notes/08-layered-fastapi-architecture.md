# 3.1 FastAPI 分层结构：router、service、repository、schema、model

## Core Idea

FastAPI 分层架构的目的不是把文件拆得更多，而是让每一层只承担一种变化原因：

- `router` 负责 HTTP 边界：路由、状态码、依赖注入、把业务异常转换成 HTTP 响应。
- `schema` 负责 API 输入输出契约：请求体校验、响应数据结构、对外字段。
- `service` 负责业务流程和业务规则：创建用户、查询用户、处理业务失败。
- `repository` 负责数据库访问：封装 `select()`、`add()`、`flush()` 等 SQLAlchemy 细节。
- `model` 负责数据库结构和 ORM 映射：表名、字段、约束、关系。
- `db/session` 负责数据库基础设施：`engine`、`AsyncSessionLocal`、`Base`、建表或迁移入口。

一个常用判断：

- 如果代码关心 `status_code`、`Depends`、`HTTPException`，多半属于 `router`。
- 如果代码关心业务语义和失败规则，多半属于 `service`。
- 如果代码关心 `select()`、`add()`、`flush()`、`commit()`，多半属于数据库边界。

## Request Flow

以 `POST /users` 为例：

```text
HTTP request
-> router 接收请求，并让 FastAPI/Pydantic 校验 UserCreate
-> service 执行业务流程 create_user
-> repository 创建 User ORM 对象并 flush
-> SQLAlchemy model 映射到 users 表
-> service commit
-> router 把 ORM User 转成 UserRead 返回
```

`schema` 的输入校验通常由 FastAPI 自动触发。比如 `UserCreate.name` 设置了 `min_length=2`，请求体不合法时，FastAPI 会在进入路由函数前直接返回 `422 Unprocessable Entity`。

## Schema And ORM Conversion

`UserRead.model_validate(user)` 的作用是把 SQLAlchemy ORM 对象转换成 Pydantic 响应模型：

```python
User(id=1, name="alice") -> UserRead(id=1, name="alice")
```

在 Pydantic v2 中，配合下面配置使用：

```python
model_config = ConfigDict(from_attributes=True)
```

这表示 Pydantic 可以从对象属性读取字段，而不只从字典读取字段。

默认情况下，schema 字段名要和 ORM model 属性名一致：

```python
class User(Base):
    id: Mapped[int]
    name: Mapped[str]

class UserRead(BaseModel):
    id: int
    name: str
```

如果对外字段名和内部字段名不同，可以用 `Field(alias=...)`，但学习阶段先保持一致更清楚。

`UserRead.from_orm(user)` 是 Pydantic v1 的旧写法；当前项目使用 `ConfigDict(from_attributes=True)`，所以更适合写 `UserRead.model_validate(user)`。

## Exception Flow

推荐的异常流：

```text
IntegrityError
-> service 转换成 UserNameConflictError
-> router 转换成 HTTP 409
```

另一条查询失败流：

```text
repository 返回 None
-> service 转换成 UserNotFoundError
-> router 转换成 HTTP 404
```

数据库连接、SQL 执行等基础设施错误可以让 `SQLAlchemyError` 向上抛，由 router 或全局 exception handler 转换成 `HTTP 500`。

关键边界：

- `repository` 不应该知道 HTTP，也不应该抛 `HTTPException`。
- `service` 不建议抛 `HTTPException`，它应该抛业务异常。
- `router` 负责把业务异常转换成 HTTP 状态码和响应内容。

## Custom Exceptions

自定义异常示例：

```python
class AppError(Exception):
    """Base class for business-level errors."""


class UserNameConflictError(AppError):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"User with name {name} already exists.")
```

`super().__init__(...)` 会把错误信息交给 Python 的 `Exception` 基类保存。之后捕获异常时：

```python
except UserNameConflictError as exc:
    detail = str(exc)
```

`str(exc)` 会读取这个异常对象里的 message。

不要在 `except` 里重新构造异常：

```python
# 不推荐
except UserNameConflictError:
    detail = UserNameConflictError(name=payload.name).args[0]
```

更好的写法：

```python
except UserNameConflictError as exc:
    raise HTTPException(status_code=409, detail=str(exc))
```

`AppError` 的作用是给业务异常建立统一家族。以后可以有 `UserNotFoundError`、`PermissionDeniedError` 等都继承它，方便统一处理业务失败。

## Session Dependency

`get_session()` 是 FastAPI dependency：

```python
async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session
```

这里容易混淆的是：`yield session` 确实把 `session` 提供给路由函数使用，但这个函数本身不是普通返回 `AsyncSession` 的函数。

只要函数体里出现 `yield`，Python 就会把它定义成生成器函数：

```python
def numbers():
    yield 1
```

调用 `numbers()` 时，拿到的不是 `1`，而是一个生成器对象。只有迭代它时，才会产生 `1`。

同理：

```python
async def get_session():
    yield session
```

因为它同时是 `async def` 并且包含 `yield`，所以它是异步生成器函数。调用它时得到的是异步生成器，不是直接得到 `session`。

类型标注：

```python
AsyncIterator[AsyncSession]
```

意思是：这个异步生成器会异步地产生一个 `AsyncSession`。

FastAPI 对这种 dependency 有特殊处理：

```text
请求开始
-> 进入 async with，创建 session
-> 执行到 yield，把 session 交给 router 使用
-> router/service/repository 执行
-> 请求结束
-> 回到 yield 后面
-> 退出 async with，自动关闭 session
```

这里的“迭代/推进生成器”不是我们手写 `for` 或 `async for` 完成的，而是 FastAPI 的依赖注入系统完成的。

```python
session: AsyncSession = Depends(get_session)
```

`Depends(get_session)` 本身更像一个声明：告诉 FastAPI 这个参数需要由 `get_session` 提供。真正执行依赖、推进异步生成器、拿到 `yield` 出来的 `session`、并在请求结束后关闭生成器的，是 FastAPI 内部的 dependency resolver。

可以用这个近似心智模型理解：

```python
gen = get_session()
session = await anext(gen)

try:
    await endpoint(session=session)
finally:
    await gen.aclose()
```

实际源码更复杂，但核心思想相同：`yield` 出来的值会被注入到 endpoint 参数里，请求结束后 FastAPI 会继续执行清理阶段。

所以 `yield` 和 `return` 的区别：

- `return session`：函数结束，不能回来执行清理逻辑。
- `yield session`：函数暂停，把 session 交出去；请求结束后还能回来收尾。

## Commit And Expiration

`commit()` 不等于关闭 session。

```text
commit = 提交当前事务
close = 关闭 session
```

在 `async with AsyncSessionLocal() as session` 生命周期内，commit 后 session 仍然可以继续使用。但一次请求中最好保持清晰的事务边界：成功 commit，失败 rollback，请求结束自动 close。

`expire_on_commit=False` 的作用是：commit 后不要把 ORM 对象字段标记为过期。

SQLAlchemy ORM 对象虽然是 Python 对象，但它的字段访问受 SQLAlchemy 管理。默认情况下，commit 后 ORM 对象可能被标记为 expired；之后访问 `user.name` 时，SQLAlchemy 可能隐式发起一次数据库查询来刷新数据。

同步 SQLAlchemy 中这通常还能工作；异步 SQLAlchemy 中，属性访问 `user.name` 不能 `await`，如果背后触发异步数据库 IO，就容易出问题。因此 FastAPI + AsyncSession 项目里常用：

```python
expire_on_commit=False
```

这样 commit 后仍然可以安全地把 `user` 转成 `UserRead`。

## Table Creation

当前 demo 可以把建表函数放在 `app/db/session.py`：

```python
async def create_all_tables() -> None:
    from app.models import users

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

必须 import models，否则 SQLAlchemy 不知道有哪些 ORM 表已经注册到 `Base.metadata`。

demo 阶段可以在 FastAPI lifespan/startup 中调用 `create_all_tables()`；正式项目更推荐 Alembic migration，不建议应用每次启动自动 `create_all()`。

## Naming

`payload` 在 API 语境里表示请求或消息携带的数据主体，不是“支付路径”。

例如：

```http
POST /users

{"name": "alice"}
```

这个 JSON body 就是 payload。

在业务语义明确时，可以用更具体的名字：

```python
async def create_user_endpoint(user_in: UserCreate):
    ...
```

`payload` 比较通用，`user_in` 更能表达“创建用户的输入数据”。

## Current Refactor Checklist

- router 中捕获异常时使用 `except ... as exc`。
- 使用 `detail=str(exc)`，不要重新构造异常。
- service 捕获 `IntegrityError` 后执行 `await session.rollback()`。
- 可以使用 `raise UserNameConflictError(name) from exc` 保留原始异常链。
- `main.py` 中把 `include_router()` 放进 `create_app()`。
- 删除不可达的 `raise NotImplementedError`。
- 删除多余的 `pass`、未使用 import、旧 TODO。
- 修复或删除乱码注释。

## My Understanding

分层结构的关键不是文件名，而是边界：HTTP 相关的东西留在 router，业务语义留在 service，数据库查询细节留在 repository，表结构留在 model，输入输出契约留在 schema。异常流也应该沿着这个边界转换：数据库异常先变成业务异常，业务异常再在 HTTP 边界变成状态码。
