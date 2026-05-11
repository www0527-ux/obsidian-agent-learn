# 第一章复盘：后端开发基本心智模型中的问题清单

## 范围

本复盘覆盖模块 1 已学习内容：

- [[../notes/01-http-asgi-fastapi-lifecycle]]
- [[../notes/02-path-operations-dependencies-structure]]
- [[../notes/03-pydantic-validation-serialization]]
- [[../notes/04-error-status-middleware-logging]]

这篇不重复整理所有知识点，只记录学习过程中真正产生过疑问、卡顿和需要后续巩固的地方。

## 1. HTTPException 与普通 return 的区别

遇到的问题：

- 为什么不能用 `200` 返回所有错误？
- `raise HTTPException(...)` 和 `return {"error": "..."}` 的本质区别是什么？

当前澄清：

- `200` 表示请求成功，不能承载所有失败语义。
- `HTTPException` 的作用不是“让机器报错”，而是把业务失败翻译成符合 HTTP 语义的错误响应。
- 例如资源不存在应返回 `404`，用户名冲突应返回 `409`。

仍需巩固：

- 在真实项目中，`HTTPException` 更偏 HTTP 层；service 层可以抛业务异常，再由 router 或 exception handler 翻译成 HTTP 响应。

## 2. 409 与 422 的边界

遇到的问题：

- 用户名已存在为什么是 `409`？
- schema 校验失败为什么是 `422`？

当前澄清：

- `422`：请求体能被解析，但没有通过 schema 校验，例如字段类型错误、长度不够、数值范围不合法。
- `409`：请求格式本身可以接受，但和当前系统资源状态冲突，例如用户名已经存在。

仍需巩固：

- 复杂业务规则中，`400`、`409`、`422` 的边界需要结合 API 语义判断。

## 3. response_model 的过滤作用

遇到的问题：

- 为什么 `POST /users` 返回 dict 里有 `password`，最终响应里却没有？

当前澄清：

- `response_model=UserRead` 不只是类型标注，还会参与响应序列化和字段过滤。
- 返回值中不属于 `UserRead` 的字段会被过滤掉，例如 `password`。

仍需巩固：

- response model 还会影响 OpenAPI 文档和响应校验。

## 4. middleware 的返回值契约

遇到的问题：

- 中间件的返回值必须是 `response` 吗？
- 能不能像 endpoint 一样直接返回 dict？

当前澄清：

- HTTP middleware 最终必须返回 `Response` 类对象。
- 这个 `Response` 可以来自 `await call_next(request)`，也可以由中间件提前构造并返回。
- middleware 比 endpoint 更接近 Starlette/ASGI 层，因此不能简单依赖 FastAPI 把 dict 自动包装成响应。

仍需巩固：

- 中间件提前返回响应时，请求不会继续进入后续路由、校验和 endpoint。

## 5. await call_next(request) 与异步协程

遇到的问题：

- `await call_next(request)` 是否类似父协程等待子协程？
- 是否必须两个函数都是 `async`？

当前澄清：

- `await` 会暂停当前协程，把控制权交还给事件循环。
- 等待对象完成后，事件循环再恢复当前协程。
- 使用 `await` 的函数必须是 `async def`。
- 被 `await` 的对象必须是 awaitable，不一定肉眼上直接是某个 `async def` 函数。

仍需巩固：

- 同步 endpoint、线程池、事件循环之间的关系暂时先放到后续专题。

## 6. logger、handler、formatter 的分工

遇到的问题：

- `basicConfig` 是什么？
- 除了 `basicConfig`，还能怎么配置 logging？
- `dictConfig` 里那么多字段分别做什么？

当前澄清：

- `basicConfig` 是快速默认配置，适合 demo。
- `dictConfig` 是显式配置，适合真实项目。
- formatter 管日志长什么样。
- handler 管日志输出到哪里。
- logger 管哪个模块的日志、以什么级别、交给哪些 handler。

当前心智模型：

```text
logger.info(...)
-> logger 级别过滤
-> handler 接收日志事件
-> formatter 格式化日志文本
-> handler 输出到终端、文件或日志系统
```

## 7. dictConfig 里的 format 字段如何取值

遇到的问题：

- `%(levelname)s`、`%(name)s`、`%(message)s` 这些值从哪里来？
- 它们是不是提前定义好的变量？

当前澄清：

- 它们不是普通变量，而是来自 logging 自动创建的 `LogRecord`。
- formatter 会按字段名从 `LogRecord` 的属性字典中取值。

近似理解：

```python
"%(levelname)s:%(name)s:%(message)s" % record.__dict__
```

字段来源：

- `name`：来自 `logging.getLogger(__name__)` 得到的 logger 名，例如 `app.main`。
- `levelname`：来自这次调用的方法，例如 `logger.info` 产生 `INFO`。
- `message`：来自 `msg + args` 格式化后的结果。
- `pathname`、`lineno`、`funcName`：来自调用日志的代码位置。

重要修正：

- `dictConfig` 里的 `"level": "INFO"` 不是给 `record.levelname` 赋值。
- 它只是过滤门槛，表示允许 `INFO` 及以上级别通过。

## 8. logger.info 里的 msg 和 args

遇到的问题：

- `logger.info(...)` 里的参数最终如何变成 `msg` 和 `args`？
- `args` 的全称是什么？

当前澄清：

- `args` 是 `arguments`，表示参数。
- `logger.info(msg, *args, **kwargs)` 中，第一个位置参数是 `msg`，后续普通位置参数进入 `args`。

示例：

```python
logger.info(
    "%s %s -> %s in %.4fs",
    request.method,
    request.url.path,
    response.status_code,
    duration,
)
```

近似生成：

```python
record.msg = "%s %s -> %s in %.4fs"
record.args = (
    request.method,
    request.url.path,
    response.status_code,
    duration,
)
```

特殊关键字参数如 `exc_info=True`、`extra={...}`、`stack_info=True` 不进入 `args`，它们用于控制日志行为或扩展 `LogRecord`。

## 9. 教学过程中的一次偏差

遇到的问题：

- 对 `dictConfig` formatter 取值机制的解释一开始没有击中真正困惑点。

当前澄清：

- 学习者已经理解 `"%s"` 按位置格式化。
- 真正困惑的是 `%(levelname)s` 这种字段名如何从 `LogRecord` 中取值。
- 后续遇到类似问题，应先区分“消息模板格式化”和“整条日志 formatter 格式化”是不是同一层。

## 后续待巩固问题

- 用一个最小例子观察 `DEBUG` 被 `"level": "INFO"` 过滤掉。
- 添加 `request_id`，观察同一个 id 如何同时进入响应 header 和日志。
- 学习 exception handler，把业务异常统一翻译成 HTTP 响应。
- 后续专题再处理同步 endpoint、线程池、事件循环之间的关系。
