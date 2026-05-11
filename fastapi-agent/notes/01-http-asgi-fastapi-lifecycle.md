# HTTP、ASGI 与 FastAPI 请求生命周期

## 核心想法

FastAPI 应用本质上是一个 ASGI 应用：服务器收到 HTTP 请求后，把请求转换成 ASGI 事件，FastAPI 根据路由、依赖、验证和业务函数生成响应。理解这条链路，后面学依赖注入、数据库 session、错误处理、Agent API 都会更稳。

## 关键点

- HTTP 是客户端和服务端之间的请求-响应协议。
- ASGI 是 Python Web 服务器和 Python Web 应用之间的通信/接口规范。
- ASGI 本身是规范，不是应用；符合 ASGI 规范的应用叫 ASGI app。
- Uvicorn 是常见 ASGI server，FastAPI 创建出来的 `app = FastAPI()` 是 ASGI app。
- 一个请求大致经过：server -> middleware -> router -> dependency -> validation -> endpoint -> serialization -> response。
- 后端调试时要区分：网络层问题、路由匹配问题、请求体验证问题、业务逻辑问题、响应序列化问题。

## 为什么叫后端心智模型

后端心智模型就是脑子里对“一个请求进入系统后如何被处理”的地图。学后端不能只记住路由、schema、ORM、CRUD、依赖注入这些零散词，而要知道它们分别处在请求生命周期的哪个位置。

一个简单版本是：

```text
客户端发来请求
-> 后端接收请求
-> 找到对应接口
-> 校验参数和请求体
-> 执行业务逻辑
-> 可能读写数据库、文件、LLM 或 Agent
-> 返回响应
```

所以 FastAPI 不只是 `@app.get()`、`@app.post()` 的写法，而是在帮我们组织“请求如何进入业务系统，又如何被响应出去”。

## ASGI 到底是什么

ASGI 可以理解成 Uvicorn 和 FastAPI 之间的共同语言：

```text
浏览器 / Postman / 前端
        |
        | HTTP
        v
Uvicorn 服务器
        |
        | ASGI
        v
FastAPI 应用
```

更准确地说：

- HTTP 是客户端和服务器之间的协议。
- ASGI 是 Python 服务器和 Python 应用之间的接口规范。
- ASGI server 是能运行 ASGI app 的服务器，例如 Uvicorn。
- ASGI app 是符合 ASGI 规范的应用，例如 `FastAPI()` 创建出的 `app`。

ASGI 核心规定了三个东西：

```text
scope
receive
send
```

一个最底层的 ASGI 应用大致长这样：

```python
async def app(scope, receive, send):
    ...
```

- `scope`：描述这次连接/请求的基本信息，比如请求类型、路径、方法、headers。
- `receive`：应用从服务器接收请求事件，比如读取请求体。
- `send`：应用把响应事件交回服务器，比如返回状态码、headers、body。

平时写 FastAPI 不需要手写这些底层接口，因为 FastAPI 已经把它包装成路由函数、依赖注入、Pydantic 校验和响应模型。

## 示例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EchoRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
async def echo(request: EchoRequest):
    return {
        "received": request.message,
        "length": len(request.message),
    }
```

访问 `/health` 时，Uvicorn 接收请求，FastAPI 匹配 `GET /health`，调用 `health()`，再把字典序列化成 JSON 响应。

访问 `/echo` 时，如果请求体是：

```json
{
  "message": "hello"
}
```

FastAPI 会根据 `request: EchoRequest` 判断：这个参数应该来自请求体，并且要用 `EchoRequest` 这个 Pydantic 模型校验。校验成功后，传入 endpoint 的 `request` 已经不是原始 JSON，而是一个 `EchoRequest` 对象，所以可以用 `request.message` 访问字段。

如果请求体写成：

```json
{
  "text": "hello"
}
```

FastAPI 会在进入 `echo()` 函数之前返回 422，因为请求体能被解析成 JSON，但不符合 `EchoRequest` 要求的字段结构。

## `/echo` 请求生命周期

```text
客户端发送 POST /echo
-> Uvicorn 接收 HTTP 请求
-> Uvicorn 按 ASGI 规范把请求交给 FastAPI
-> FastAPI 匹配到 @app.post("/echo")
-> FastAPI 分析 echo(request: EchoRequest)
-> 判断 request 来自请求体 body
-> 读取 JSON body
-> 用 EchoRequest 进行 Pydantic 校验
-> 校验失败：直接返回 422
-> 校验成功：创建 EchoRequest 对象
-> 调用 echo(request)
-> endpoint 返回 Python dict
-> FastAPI 把 dict 序列化成 JSON
-> Uvicorn 把 HTTP 响应发回客户端
```

## 关联

- 相关概念：[[02-path-operations-dependencies-structure]]
- 前置于：[[03-pydantic-validation-serialization]]
- 前置于：[[../projects/demos/01-minimal-fastapi-api]]

## 我的理解

- ASGI 是 Python Web 服务器和 Python Web 应用之间的通信规范。
- ASGI 本身是规范；符合这个规范的应用叫 ASGI app，能运行这种应用的服务器叫 ASGI server。
- 在本 demo 中，Uvicorn 是 ASGI server，`app = FastAPI()` 创建出来的是 ASGI app。
- `request: EchoRequest` 不只是类型提示，它会参与 FastAPI 的运行时行为：FastAPI 会从请求体读取 JSON，并用 `EchoRequest` 校验。
- 如果校验失败，FastAPI 不会进入 endpoint，而是自动返回 422。
