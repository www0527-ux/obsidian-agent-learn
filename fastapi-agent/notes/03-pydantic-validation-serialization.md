# Pydantic schema、数据校验、序列化与响应模型

## 核心想法

1.3 要理解的是：后端接口面对的是外部传来的数据，外部数据天然不可信。Pydantic schema 的作用，就是把不可靠的 JSON 转成有结构、有类型、可校验的 Python 对象；响应模型则负责把后端返回的数据整理成稳定、安全、符合接口约定的输出。

## 关键点

- schema 描述接口数据的结构。
- 请求 schema 负责校验客户端传进来的数据。
- 响应 schema 负责约束接口返回给客户端的数据。
- 数据校验发生在进入路由函数之前。
- 序列化发生在返回响应时，把 Python 对象转换成 JSON 可表达的数据。
- 请求模型和响应模型通常要分开，不要一个模型到处复用。
- Pydantic 不只做类型校验，也能做字段约束、默认值、嵌套结构校验和自定义业务规则校验。

## 请求 schema

请求 schema 用来描述客户端应该传什么。

```python
from pydantic import BaseModel

class EchoRequest(BaseModel):
    message: str
```

如果路由函数写成：

```python
@app.post("/echo")
async def echo(request: EchoRequest):
    return {"received": request.message}
```

FastAPI 会根据 `request: EchoRequest` 判断：这个参数来自请求体，并且要用 `EchoRequest` 进行校验。

## 数据校验

比如模型要求：

```python
class CreateUserRequest(BaseModel):
    username: str
    age: int
```

合法请求：

```json
{
  "username": "alice",
  "age": 18
}
```

不合法请求：

```json
{
  "username": "alice"
}
```

因为缺少 `age`。FastAPI 会在进入 endpoint 之前返回 422。

## 不只是类型校验

Pydantic 的校验可以分成几层。

### 1. 必填字段与可选字段

```python
class CreateUserRequest(BaseModel):
    username: str
    nickname: str | None = None
```

- `username` 必须传。
- `nickname` 可以不传；不传时默认是 `None`。

注意：`str | None` 表示类型上允许为空，但如果没有默认值，它仍然可能是必填字段。更常见的可选写法是：

```python
nickname: str | None = None
```

### 2. 默认值

```python
class CreateTodoRequest(BaseModel):
    title: str
    completed: bool = False
```

客户端可以只传：

```json
{
  "title": "learn FastAPI"
}
```

校验后得到的对象里，`completed` 会自动是 `False`。

### 3. 字段约束

可以用 `Field()` 给字段加更细的限制：

```python
from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=0, le=150)
```

含义：

- `username` 长度至少 3，最多 20。
- `age` 大于等于 0，小于等于 150。

这类约束会自动体现在 `/docs` 里，也会自动参与 422 错误响应。

### 4. 字符串、数字、列表约束

常见约束包括：

```python
class CreateCourseRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    difficulty: int = Field(ge=1, le=5)
    tags: list[str] = Field(default_factory=list, max_length=5)
```

`default_factory=list` 用来给列表创建默认空列表。不要把可变对象直接写成默认值，这是 Python 里很容易踩的坑。

### 5. 嵌套模型

schema 可以嵌套：

```python
class Author(BaseModel):
    name: str
    email: str

class ArticleCreate(BaseModel):
    title: str
    content: str
    author: Author
```

对应请求体：

```json
{
  "title": "FastAPI note",
  "content": "schema is contract",
  "author": {
    "name": "alice",
    "email": "alice@example.com"
  }
}
```

FastAPI 会递归校验 `author` 里面的字段。

### 6. 自定义校验

有些规则不是单纯的类型或长度能表达的，比如“用户名不能包含空格”。Pydantic v2 可以用 `field_validator`：

```python
from pydantic import BaseModel, field_validator

class CreateUserRequest(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def username_must_not_contain_space(cls, value: str) -> str:
        if " " in value:
            raise ValueError("username must not contain spaces")
        return value
```

如果传入：

```json
{
  "username": "alice test"
}
```

校验会失败，FastAPI 返回 422。

### 7. 跨字段校验

有些规则需要同时看多个字段，比如确认密码：

```python
from pydantic import BaseModel, model_validator

class RegisterRequest(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self
```

这类校验适合处理“字段之间的关系”。

## 序列化

序列化就是把 Python 对象转换成可以通过网络传输的格式，通常是 JSON。

例如 endpoint 返回：

```python
return {"id": 1, "username": "alice"}
```

客户端收到的是 JSON：

```json
{
  "id": 1,
  "username": "alice"
}
```

如果返回值里有 `datetime`、`UUID`、Pydantic model 等对象，FastAPI/Pydantic 也会尝试把它们转成 JSON 可表示的形式。

## 响应模型

响应模型用 `response_model` 声明接口返回的数据结构。

```python
class UserResponse(BaseModel):
    id: int
    username: str

@app.post("/users", response_model=UserResponse)
async def create_user(request: CreateUserRequest):
    return {
        "id": 1,
        "username": request.username,
        "password_hash": "secret"
    }
```

虽然 endpoint 返回了 `password_hash`，但因为 `response_model=UserResponse` 没有这个字段，FastAPI 返回给客户端时会过滤掉它。

这里要注意：`response_model=UserResponse` 不是路由函数的参数，而是 `@app.post()` 这个路由装饰器的参数。它告诉 FastAPI：“这个接口对外返回的数据结构应该按 `UserResponse` 处理。”

也可以用返回类型标注表达类似含义：

```python
@app.post("/users")
async def create_user(request: CreateUserRequest) -> UserResponse:
    return {
        "id": 1,
        "username": request.username,
        "password_hash": "secret"
    }
```

不过在 FastAPI 项目里，`response_model=UserResponse` 很常见，因为它是明确写给 FastAPI 路由系统看的；`-> UserResponse` 更像 Python 类型标注，同时 FastAPI 也能读取它来生成响应模型。

这说明响应模型有两个作用：

- 约束接口输出结构。
- 避免把内部字段泄露给客户端。

## 422 错误结构怎么看

校验失败时，FastAPI 返回的 422 通常会包含 `detail`，里面说明错误位置、错误类型和错误信息。例如缺少字段时，结构大致是：

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "message"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

重点看：

- `loc`：错误发生在哪里，比如 `body.message`。
- `type`：错误类型，比如缺字段、类型错误、长度不符合。
- `msg`：人类可读的错误说明。

调试请求体验证问题时，先看 `loc`，再看 `type`。

## 常见设计建议

- 请求模型和响应模型分开，例如 `UserCreate`、`UserRead`。
- 不要直接把数据库 ORM model 当作 API schema。
- 不要把密码、token、内部状态字段放进响应模型。
- 对外 API 的字段要稳定，内部数据库字段可以变化。
- schema 名字尽量表达用途，例如 `LearningSessionCreate`、`LearningSessionRead`、`LearningSessionUpdate`。
- 对 `Update` 模型，字段通常是可选的，因为 PATCH/局部更新不要求传全部字段。

## 请求模型和响应模型为什么要分开

创建用户时，客户端可能只需要传：

```python
class UserCreate(BaseModel):
    username: str
    password: str
```

但返回给客户端时，不应该返回密码：

```python
class UserRead(BaseModel):
    id: int
    username: str
```

所以请求模型和响应模型关注的问题不同：

- 请求模型：客户端需要提供什么。
- 响应模型：后端允许暴露什么。

## 与请求生命周期的关系

```text
请求进入
-> FastAPI 匹配路由
-> 根据函数参数找到请求 schema
-> 读取请求体
-> Pydantic 校验并生成 Python 对象
-> 调用 endpoint
-> endpoint 返回 Python 对象
-> 根据 response_model 过滤/转换返回值
-> 序列化成 JSON
-> 返回客户端
```

## 我的理解

待补充：用自己的话解释“请求 schema 和响应 schema 分别解决什么问题”。
