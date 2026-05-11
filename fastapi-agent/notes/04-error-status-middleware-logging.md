# 错误处理、状态码、中间件与日志

## 核心想法

1.4 要理解的是：后端接口不只是成功返回数据，还要能在失败时给出清晰、稳定、符合语义的响应。状态码负责表达结果类型，错误处理负责把异常转换成 API 响应，中间件负责在请求前后做统一处理，日志负责记录系统运行过程，帮助调试和排查问题。

## 关键点

- 状态码是 API 和客户端之间的结果信号。
- `2xx` 通常表示成功，`4xx` 表示客户端请求有问题，`5xx` 表示服务端内部错误。
- `HTTPException` 用来主动返回符合 API 语义的错误响应。
- 校验失败时，FastAPI/Pydantic 会自动返回 `422`。
- 中间件可以包裹整个请求生命周期，在请求进入 endpoint 前后执行逻辑。
- 日志用于记录请求、错误、关键业务事件和调试信息。

## 常见状态码

```text
200 OK：请求成功。
201 Created：资源创建成功。
204 No Content：成功，但没有响应体。
400 Bad Request：请求格式或参数整体有问题。
401 Unauthorized：未认证。
403 Forbidden：已认证，但没有权限。
404 Not Found：资源不存在。
409 Conflict：资源冲突，例如用户名已存在。
422 Unprocessable Entity：请求体能解析，但不符合 schema 校验。
500 Internal Server Error：服务端内部错误。
```

状态码的作用不是装饰，而是让客户端不用解析所有响应内容，也能先知道结果大类。

## 主动抛出 HTTPException

当业务上明确要返回错误时，不要随便 `return {"error": "xxx"}`，而是用 `HTTPException`：

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": 1, "username": "alice"}
```

这样客户端会收到真正的 `404`，而不是 `200` 加一个错误消息。

## 业务错误和程序错误

要区分两类错误：

```text
业务错误：资源不存在、权限不足、用户名冲突、参数不符合业务规则。
程序错误：代码 bug、数据库连接失败、未处理异常。
```

业务错误应该被转换成明确的 `4xx` 响应。

程序错误通常不应该把内部细节暴露给客户端，生产环境里一般返回 `500`，同时把详细错误写入日志。

## 深入：错误响应设计的三层问题

设计 API 错误时，不要只问“返回什么字符串”，而要分三层看：

```text
第一层：HTTP 状态码
这次请求的大类结果是什么？成功、未认证、无权限、资源不存在、冲突、校验失败、服务端异常？

第二层：错误响应体
客户端或前端需要哪些稳定字段来展示、判断和调试？例如 code、message、detail、request_id。

第三层：服务端日志
开发者需要哪些上下文来排查问题？例如路径、方法、状态码、耗时、用户 ID、异常堆栈、request_id。
```

一个常见的错误响应体可以长这样：

```json
{
  "code": "USER_NOT_FOUND",
  "message": "User not found",
  "detail": {
    "user_id": 123
  },
  "request_id": "req_abc123"
}
```

这里的重点是：状态码给机器判断大类，`code` 给客户端稳定分支，`message` 给人读，`detail` 放必要但不敏感的上下文，`request_id` 用来把客户端报错和服务端日志串起来。

## 深入：什么时候用 400、404、409、422

这些状态码容易混在一起，可以用下面的判断方式：

```text
400：请求整体语义有问题，或者多个字段组合后不符合接口规则。
404：客户端请求的是某个资源，但这个资源不存在。
409：请求本身格式没错，但和当前系统状态冲突。
422：请求体能被解析，也进入了 schema 校验，但字段不符合 schema 规则。
```

例子：

- `GET /users/123`，系统没有 123 号用户：`404`
- `POST /users`，username 已经存在：`409`
- `POST /users`，username 只有 1 个字符，被 Pydantic 拦下：`422`
- `POST /transfer`，from_account 和 to_account 是同一个账户：常见做法是 `400`

## 深入：HTTPException 应该出现在哪里

在小 demo 里，直接在 endpoint 里 `raise HTTPException` 没问题。但在更真实的项目里，常见结构是：

```text
router / endpoint：负责 HTTP 输入输出，把业务错误翻译成 HTTPException
service：负责业务规则，通常抛业务异常或返回业务结果
repository：负责数据库访问
```

也就是说，`HTTPException` 是偏 HTTP 层的东西。越靠近 service 和 repository，越应该少知道 FastAPI 的细节。这样未来即使把业务逻辑用在 CLI、后台任务、Agent tool 中，也不会被 Web 框架绑死。

## 深入：中间件、异常处理器和日志的分工

三者经常一起出现，但职责不同：

```text
中间件 middleware：
包裹请求前后，适合统一记录耗时、添加 request_id、设置 header。

异常处理器 exception handler：
把某类异常统一转换成响应，适合统一错误响应格式。

日志 logging：
记录发生了什么，给开发和运维排查问题。
```

中间件像入口和出口的门岗，异常处理器像翻译员，日志像运行记录。三者配合起来，API 才既对客户端友好，又对开发者可排查。

## 中间件是什么

中间件是在请求进入 endpoint 之前、响应返回客户端之前执行的一层包装。

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = str(duration)
    return response
```

它的流程是：

```text
请求进入
-> middleware 前半段
-> 路由匹配、校验、依赖、endpoint
-> middleware 后半段
-> 响应返回
```

中间件常用于：

- 记录请求耗时
- 添加统一响应 header
- 处理 CORS
- 请求 ID / trace ID
- 统一日志
- 简单认证或安全处理

## 日志是什么

日志是给开发者和运维看的，不是给客户端看的。

```python
import logging

logger = logging.getLogger(__name__)

@app.get("/health")
async def health():
    logger.info("health check")
    return {"status": "healthy"}
```

日志应该记录：

- 请求进入和结束
- 关键业务动作
- 异常和堆栈
- 慢请求
- 外部服务调用失败

不要在日志里记录明文密码、token、敏感个人信息。

## 深入：dictConfig 怎么读

`logging.basicConfig(...)` 是快速配置，适合小 demo。`dictConfig(...)` 是显式配置，适合真实项目，因为它能分别控制：

```text
formatter：日志长什么样
handler：日志输出到哪里
logger：哪个模块的日志，用什么 handler，以什么级别输出
```

一次日志调用可以这样理解：

```text
logger.info("GET /health -> 200")
-> logger 判断 INFO 级别是否允许输出
-> 交给 handler
-> handler 用 formatter 把日志格式化
-> handler 输出到终端、文件或日志系统
```

示例：

```python
dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)s:%(name)s:%(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "httpx": {
            "level": "WARNING",
        },
    },
})
```

字段含义：

- `version: 1`：配置格式版本，目前固定写 `1`。
- `disable_existing_loggers: False`：不要把已经存在的第三方 logger 全部禁用。
- `formatters.default.format`：定义日志文本格式，例如级别、logger 名、消息。
- `handlers.console.class`：使用 `StreamHandler`，表示输出到终端。
- `handlers.console.formatter`：这个 handler 使用名为 `default` 的 formatter。
- `loggers.app`：配置所有名字以 `app` 开头的 logger，例如 `app.main`。
- `loggers.app.level`：允许 `INFO` 及以上日志输出。
- `loggers.app.propagate: False`：日志不再继续往父 logger 传，避免重复输出。
- `loggers.httpx.level: WARNING`：第三方 `httpx` 只显示 warning/error，隐藏普通 info 请求日志。

`logger = logging.getLogger(__name__)` 会根据当前模块名创建 logger。当前 demo 被导入为 `app.main` 时，logger 名就是 `app.main`，它会匹配 `loggers.app` 这条配置。

## 深入：日志级别和 format 字段从哪里来

调用日志时：

```python
logger.info("GET /health -> 200")
```

logging 内部会创建一个 `LogRecord` 对象。这个对象里提前放好了很多字段，例如：

```text
levelname：日志级别名称，例如 INFO、WARNING、ERROR
name：logger 的名字，例如 app.main
message：最终日志消息
asctime：日志时间
pathname：产生日志的文件路径
lineno：产生日志的代码行号
funcName：产生日志的函数名
```

所以 formatter 里的：

```python
"%(levelname)s:%(name)s:%(message)s"
```

不是你自己定义的变量，而是从 `LogRecord` 里取字段：

```text
%(levelname)s -> record.levelname
%(name)s      -> record.name
%(message)s   -> record.message
```

末尾的 `s` 表示按字符串格式化。logging 默认使用这种 `%` 风格的 formatter。

常见格式：

```python
"%(levelname)s:%(name)s:%(message)s"
"%(asctime)s %(levelname)s [%(name)s] %(message)s"
"%(levelname)s %(pathname)s:%(lineno)d %(message)s"
```

这里的 `%(lineno)d` 用 `d`，因为行号是整数。

更底层一点看，formatter 不是自己“猜”字段，而是拿到了一个 `LogRecord` 对象，并从它的属性字典里按名字取值。可以近似理解为：

```python
record.__dict__ = {
    "levelname": "INFO",
    "name": "app.main",
    "message": "GET /health -> 200 in 0.0010s",
    "pathname": ".../app/main.py",
    "lineno": 52,
    "funcName": "log_time",
}
```

然后 formatter 做的事情类似：

```python
"%(levelname)s:%(name)s:%(message)s" % record.__dict__
```

所以：

```text
%(levelname)s 按名字去 record.__dict__["levelname"] 里找
%(name)s      按名字去 record.__dict__["name"] 里找
%(message)s   按名字去 record.__dict__["message"] 里找
```

这些字段的来源大致是：

```text
name：来自 logger 的名字，例如 logging.getLogger(__name__) 得到的 app.main
levelname：来自这次日志调用本身，例如 logger.info 对应 INFO，logger.warning 对应 WARNING
message：来自 logger.info("...%s", args...) 这组 msg + args 格式化后的结果
pathname / lineno / funcName：logging 根据调用 logger.info 的代码位置自动计算
asctime：如果 format 里需要时间，formatter 会额外计算
```

注意：`dictConfig` 里 `"level": "INFO"` 的作用不是给 `record.levelname` 填值，而是设置过滤门槛。

```text
logger.info(...)     -> 这次日志事件的 levelname 是 INFO
logger.warning(...)  -> 这次日志事件的 levelname 是 WARNING

"level": "INFO"      -> 允许 INFO 及以上日志通过
"level": "WARNING"   -> 只允许 WARNING 及以上日志通过
```

也就是说，日志级别配置决定“这条日志能不能出来”，而具体的 `levelname` 来自你调用了 `logger.info`、`logger.warning` 还是 `logger.error`。

因此 `dictConfig` 里的 `format` 本质上是声明：“等每次日志事件来了，请从这条日志事件的 `LogRecord` 字段中按名字取值，并拼成这个样子。”

日志级别从低到高：

```text
DEBUG：调试细节，开发时看
INFO：正常运行信息，例如一次请求完成
WARNING：可疑情况，但程序还能继续
ERROR：某次操作失败
CRITICAL：严重错误，系统可能无法继续
```

设置：

```python
"level": "INFO"
```

表示这个 logger 允许输出 `INFO`、`WARNING`、`ERROR`、`CRITICAL`，但不会输出更低级别的 `DEBUG`。

## 与请求生命周期的关系

```text
请求进入
-> middleware 前半段
-> router 匹配
-> 参数解析和 Pydantic 校验
-> 依赖注入
-> endpoint 执行业务
-> 可能主动 raise HTTPException
-> FastAPI 把异常转换成响应
-> middleware 后半段
-> 日志记录结果
-> 响应返回客户端
```

## 我的理解

不能用 `200` 返回所有错误，因为 `200` 在 HTTP 语义里表示请求成功。即使响应体里写了 `{"error": "User not found"}`，客户端、浏览器、网关、监控系统、SDK 仍然会先把它当作成功响应处理。

更合适的做法是用 `HTTPException` 把业务失败翻译成明确的 HTTP 错误响应，例如资源不存在返回 `404`，资源冲突返回 `409`。这样客户端可以先根据状态码判断大类，再根据响应体里的 `detail` 或错误码做具体处理。

`422` 和 `409` 的区别：`422` 主要是请求数据没有通过 schema 校验；`409` 是请求格式本身可以接受，但和当前系统资源状态冲突。

middleware 负责包裹每个请求，适合统一计时、添加 request id、记录访问日志；`HTTPException` 负责把业务失败转换成 HTTP 错误响应；logging 负责在服务端记录运行过程、错误和排查上下文。
