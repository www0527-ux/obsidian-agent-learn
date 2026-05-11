from fastapi import FastAPI
from pydantic import BaseModel,Field,field_validator
from fastapi import HTTPException,Request
import time
import logging
from logging.config import dictConfig

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,#保留现有的日志记录器配置
    "formatters": {
        "default": {
            "format": "%(levelname)s:%(name)s:%(message)s",#logging内部定义的占位符，分别表示日志级别、记录器名称和日志消息
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
logger=logging.getLogger(__name__)#参数就是logger的名字，通常使用__name__，这样日志记录器就会以模块名命名


app= FastAPI()
class EchoRequest(BaseModel):
    message: str
class Usercreate(BaseModel):
    username: str=Field(max_length=20,min_length=3)
    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if " " in value:
            raise ValueError("Username should not contain spaces")
        return value
    age: int=Field(gt=0, lt=150)
    password: str=Field(min_length=8)
    tags: list[str]=Field(max_length=5)#列表个数最多为五

class UserRead(BaseModel):
    id: int
    username: str
    age: int
    tags: list[str]

@app.middleware("http")
async def log_time(request:Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["X-Process-Time"] = str(duration)
    logger.info(
        "%s %s -> %s in %.4fs",
        request.method,
        request.url.path,
        response.status_code,
        duration
    )#转换成msg和args的形式，msg是一个格式化字符串，args是一个元组，包含了要插入到格式化字符串中的值
    return response


@app.get("/health")
async def health():
    return{"status": "healthy"}

@app.post("/echo")
async def echo(request: EchoRequest):
    return{"received": request.message,
           "length": len(request.message)
           }
@app.post("/users",response_model=UserRead)
async def create_user(user: Usercreate):
    # 模拟用户创建逻辑
    if user.username == "alice":
        raise HTTPException(status_code=409, detail="Username already exists")
    return {
    "id": 1,
    "username": user.username,
    "age": user.age,
    "tags": user.tags,
    "password": "********"
    }
@app.get("/users/{user_id}",response_model=UserRead)
async def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {
    "id": user_id,
    "username": "testuser",
    "age": 30,
    "tags": ["example", "demo"]
    }
