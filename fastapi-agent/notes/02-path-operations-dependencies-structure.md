# 路由函数、依赖注入与应用结构

## 核心想法

1.2 这一节要理解 FastAPI 如何把一个 HTTP 请求分发给具体的 Python 函数，以及如何用依赖注入把“公共资源”交给这个函数。路由函数负责描述接口入口，依赖注入负责准备运行这个接口所需要的对象，应用结构负责让项目在变大后仍然清楚。

## 关键点

- 路由函数，也叫 path operation function，是处理某个 HTTP 方法 + 路径组合的函数。
- 装饰器如 `@app.get("/health")`、`@app.post("/echo")` 会把 URL 路径和 Python 函数绑定起来。
- FastAPI 会根据函数参数判断数据来源：路径参数、查询参数、请求体、header、cookie、依赖。
- 依赖注入通过 `Depends()` 声明“这个接口运行前需要先准备什么”。
- 应用结构的目标是把入口、业务逻辑、数据访问、schema 分开，避免所有代码都堆在 `main.py`。

## 路由函数是什么

一个路由函数就是一个接口的入口：

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

这里 FastAPI 会理解：

- `GET /items/123` 会调用 `read_item()`。
- `item_id` 来自路径参数，因为路径里有 `{item_id}`。
- `q` 来自查询参数，例如 `/items/123?q=hello`。
- `item_id: int` 会触发类型转换和校验。

## 依赖注入是什么

依赖注入就是不要在接口函数内部临时创建一切，而是声明“我需要什么”，由框架在调用接口前帮你准备。

```python
from fastapi import Depends

def get_current_user():
    return {"name": "demo-user"}

@app.get("/me")
async def read_me(user = Depends(get_current_user)):
    return user
```

请求 `/me` 时，FastAPI 会先执行 `get_current_user()`，再把返回值作为 `user` 传给 `read_me()`。

依赖注入常用于：

- 获取数据库 session
- 获取当前用户
- 校验权限
- 读取配置
- 创建业务服务对象
- 复用公共查询参数

## 应用结构为什么重要

demo 可以把所有代码写在 `main.py`，但项目变大后会很快混乱。一个常见结构是：

```text
app/
├── main.py
├── api/
│   └── routes/
│       └── learning_sessions.py
├── schemas/
│   └── learning_session.py
├── services/
│   └── learning_session_service.py
├── repositories/
│   └── learning_session_repo.py
└── db/
    └── session.py
```

大致分工：

- `main.py`：创建 FastAPI app，挂载路由。
- `routes/`：定义 API 入口，处理 HTTP 层细节。
- `schemas/`：定义请求体和响应体结构。
- `services/`：写业务规则。
- `repositories/`：封装数据库读写。
- `db/`：管理数据库连接和 session。

## 与请求生命周期的关系

```text
请求进入
-> router 匹配路径和方法
-> FastAPI 分析函数参数
-> 解析路径参数、查询参数、请求体
-> 执行 Depends 声明的依赖
-> 调用路由函数
-> 路由函数调用 service / repository
-> 返回响应
```

## 我的理解

待补充：用自己的话解释“路由函数和依赖注入分别解决什么问题”。

