# 配置管理、环境变量与应用 settings

## 核心想法

1.5 要理解的是：应用代码不应该把所有运行参数都写死。数据库地址、密钥、运行环境、日志级别、第三方 API key 等信息，应该通过配置系统注入进应用。

配置管理的目标是让同一份代码可以在不同环境中运行：

```text
本地开发：使用本地数据库、DEBUG 日志、测试 key
测试环境：使用测试数据库、模拟外部服务
生产环境：使用生产数据库、正式密钥、更严格日志和安全设置
```

## 为什么不能把配置写死

不要这样：

```python
DATABASE_URL = "postgresql://user:password@prod-db/app"
SECRET_KEY = "real-secret"
DEBUG = True
```

问题：

- 密码和 key 容易被提交到代码仓库。
- 本地、测试、生产环境无法灵活切换。
- 改配置需要改代码，容易引入不必要的发布风险。
- 多人协作时，每个人的本地配置可能不同。

## 环境变量是什么

环境变量是操作系统或运行环境提供给程序的键值对。

```text
APP_ENV=development
DATABASE_URL=sqlite:///./dev.db
LOG_LEVEL=INFO
```

应用启动时读取这些变量，根据它们决定如何运行。

## settings 是什么

`settings` 通常是一个集中管理配置的对象。它把分散的环境变量转换成应用内部更好用的 Python 属性。

示例心智模型：

```python
settings.app_env
settings.database_url
settings.log_level
settings.secret_key
```

代码其他地方不直接到处读环境变量，而是统一依赖 `settings`。

## 常见配置项

- 应用环境：`APP_ENV`
- 数据库连接：`DATABASE_URL`
- 密钥：`SECRET_KEY`
- 日志级别：`LOG_LEVEL`
- 是否开启 debug：`DEBUG`
- 第三方服务 key：`OPENAI_API_KEY`、`SMTP_PASSWORD`
- CORS 允许来源：`CORS_ORIGINS`

## 与前面几节的关系

配置管理会影响前面学过的内容：

```text
1.1 请求生命周期：应用启动时先加载 settings，再处理请求。
1.2 依赖注入：可以用 Depends 注入配置、数据库连接、服务对象。
1.3 schema：配置不是请求 schema，但也需要类型校验。
1.4 日志：日志级别、日志格式、是否输出 debug 信息都应该由配置控制。
```

## 后续会怎么用

进入数据库章节后，`DATABASE_URL` 会变得很重要。进入 Agent 章节后，模型 API key、工具权限、记忆存储路径等也都属于配置。

所以 1.5 不是一个孤立小节，而是为了让后面的数据库、Agent、部署都能有一个稳定入口。

## 我的理解

待补充：用自己的话解释“为什么配置应该和代码分离”。
