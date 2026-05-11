# Demo 01：最小 FastAPI API

## 学习目标

这个 demo 对应 1.1：HTTP、ASGI 与 FastAPI 请求生命周期。目标不是写一个完整项目，而是亲手走一遍“请求进入 FastAPI 后发生了什么”。

## 你要做什么

创建一个最小 FastAPI 应用，包含两个接口：

- `GET /health`
- `POST /echo`

`GET /health` 返回：

```json
{
  "status": "ok"
}
```

`POST /echo` 接收：

```json
{
  "message": "hello"
}
```

返回：

```json
{
  "received": "hello",
  "length": 5
}
```

## 建议目录

```text
01-minimal-fastapi-api/
├── app/
│   └── main.py
├── tests/
│   └── test_main.py
└── reflection.md
```

## 推荐代码骨架

你可以先自己写，也可以参考这个骨架：

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
def echo(payload: EchoRequest):
    return {
        "received": payload.message,
        "length": len(payload.message),
    }
```

## 运行方式

第一次运行前，先创建 conda 环境：

```bash
conda env create -f environment.yml
```

之后进入环境：

```bash
conda activate fastapi-agent-demo
```

在 demo 目录里运行：

```bash
uvicorn app.main:app --reload
```

然后打开：

```text
http://127.0.0.1:8000/docs
```

## 你要观察什么

- 请求 `GET /health` 时，FastAPI 如何返回 JSON。
- 请求 `POST /echo` 时，FastAPI 如何读取请求体。
- 如果传入 `{ "text": "hello" }`，FastAPI 为什么会报 422。
- `/docs` 页面为什么能自动生成接口文档。

## 完成标准

完成后，在 `reflection.md` 里回答：

1. `uvicorn app.main:app --reload` 这行命令里的 `app.main:app` 分别指什么？
2. `EchoRequest(BaseModel)` 在请求生命周期中负责什么？
3. 为什么字段名写错时，FastAPI 能自动返回 422？
4. endpoint 返回 Python 字典后，是谁把它变成 JSON 响应的？
5. 用自己的话写一遍：一次 `/echo` 请求从进入后端到返回响应，大概经历了哪些步骤？
