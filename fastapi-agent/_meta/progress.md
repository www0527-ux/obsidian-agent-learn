# 学习进度：FastAPI + Agent

## 当前状态
<!-- BLOOM:CURRENT_STATE:START -->
- **当前模块**：模块 2：数据库与 SQLAlchemy
- **当前概念**：2.5 Alembic 迁移与数据库结构演进
- **总体掌握度**：2/42 个概念已掌握
- **学习次数**：42
- **上次学习**：2026-05-11
- **学习者水平**：中级接触者，但需要系统重建基础
- **语言**：中文
<!-- BLOOM:CURRENT_STATE:END -->

## 学习目标

通过学习 FastAPI、SQLAlchemy、后端架构、LangGraph/Agent 工作范式，逐步建立稳定的后端 + Agent 应用开发能力。最终做出一个“学习记录智能体”：它能把学习笔记、demo、复习记录和项目记录关联进 Obsidian。

## 当前基础

- 接触过 FastAPI，见过 schema、ORM、CRUD、数据库等概念。
- 了解 Agent 的几种工作范式，接触过 LangGraph。
- 主要短板：概念熟悉但不够稳，还不能算是基础扎实的 Agent 应用开发者。
- 合适路线：项目驱动 + 小 demo 拆解 + 概念笔记 + 间隔复习。

## 学习记录

<!-- BLOOM:SESSION_LOG:START -->
### 2026-05-11：2.5 新增 Alembic 文件组织范本

- 学习者反馈 Alembic 语法和环境文件显得复杂，希望先有一个可模仿的文件夹范本。
- 新增 `projects/demos/03-alembic-migration-template/`，包含 `app/db.py`、`app/models.py`、`alembic.ini`、`migrations/env.py`、`script.py.mako` 和两个示例迁移文件。
- 当前学习目标：先读懂 `models.py` 描述目标结构、`versions/*.py` 描述结构演进历史、`env.py` 把 Alembic 接到 `Base.metadata`，暂不要求运行命令。

### 2026-05-11：2.4 掌握度自测通过

- 学习者能说明 `selectinload(User.records)` 先查父对象，再用子表外键 `user_id IN (...)` 批量查 records，最后按外键归档回各自的 `User.records`，因此不会展开重复父对象，也不需要 `.unique()`。
- 能说明 `user.records.append(record)` 会在 Python 对象层同步 `record.user = user`；真正的 `record.user_id` 会在 flush/commit 时根据数据库生成的 `user.id` 写入。
- 能对比 lazy loading、`selectinload`、`joinedload`：100 个 user、每人约 3 条 records 时，lazy 是 `1 + 100 = 101` 次 SQL，`selectinload` 是 2 次 SQL，`joinedload` 是 1 次 SQL。小纠正：300 是 records 结果行数量，不是 lazy 的 SQL 次数。
- 将 `2.4 表关系、懒加载/预加载与 N+1 问题` 标记为掌握，并安排 2026-05-12 复习。下一步进入 2.5 Alembic 迁移与数据库结构演进。

### 2026-05-11：2.4 深入理解 joinedload 与 unique

- 追问并澄清 `session.scalars(stmt)`、`session.execute(stmt)`、`.unique()` 在 `joinedload(User.records)` 下的关系。
- 关键理解：`joinedload` 让一对多关系在 SQL 行层面展开；identity map 按实体类型和主键复用同一个 `User` 对象；relationship loader 把每一行里的 `LearningRecord` 填进同一个 `User.records`；`.unique()` 只负责过滤最终结果流里重复出现的父对象引用。
- 已新增笔记 [[../notes/07-relationships-loading-n-plus-one]]。
- 下一步：继续练习 `selectinload(User.records)` 的参数含义，并对比 `selectinload` 与 `joinedload` 的适用场景。

### 2026-05-11：2.4 拆分练习代码并增加预加载对比

- 将 `practice.py` 拆分为 `db.py`、`models.py`、`crud.py`、`loading_examples.py` 和入口 `practice.py`，避免单文件过长。
- 新增 `list_users_lazy()`、`list_users_with_selectinload()`、`list_users_with_joinedload()`，用于对比懒加载、批量预加载和 JOIN 风格预加载。
- 新增练习 [[../exercises/07-relationships-loading-n-plus-one]]；已运行验证三种加载方式，观察到懒加载触发多次 `SELECT learning_records WHERE user_id = ?`，`selectinload` 使用 `WHERE user_id IN (...)`，`joinedload` 使用 JOIN 并需要 `.unique()`。

### 2026-05-11：2.4 创建 User 与多条 LearningRecord

- 在 `practice.py` 中补充 `create_user(name)` 与 `create_user_with_records(name, records_data)`。
- 调整 `insert_record` 需要显式传入 `user_id`，以满足 `LearningRecord.user_id` 非空外键约束。
- 已运行验证：创建 `alice` 后插入一条记录；创建 `bob` 时通过 `user.records.append(...)` 关联两条记录，并观察到访问 `user.records` 会触发关系查询。

### 2026-05-11：2.4 relationship 与 back_populates

- 学习者已添加 `User` 表并将其与 `LearningRecord` 关联，追问 `relationship` 是否是表中的列，以及 `back_populates` 的作用。
- 反馈重点：`ForeignKey` 是数据库列，`relationship` 不是表列，而是 ORM 层的对象导航属性；`back_populates` 用来声明两边关系互相对应，保持 `user.records` 与 `record.user` 的双向同步。
- 待修正：类名建议使用 `User`；不需要在 `users` 表中存 `record_ids`，一对多关系由 `learning_records.user_id` 表达。

### 2026-05-11：开始 2.4 表关系、懒加载/预加载与 N+1 问题

- 从单表 CRUD 进入多表关系查询。
- 本节目标：理解一对多、多对一、多对多关系如何在 SQLAlchemy 中表达，以及懒加载、预加载和 N+1 问题的取舍。
- 下一步会围绕学习记录系统设计 `User -> LearningRecord` 或 `LearningRecord -> Note` 的关系 demo。

### 2026-05-11：2.3 掌握度自测通过

- 学习者完成 2.3 收尾自测：能说明 update 前先查询是为了确认记录存在并返回真实错误原因；能区分 ORM 对象删除与条件 DELETE；能说明 `None/False` 在 FastAPI 层通常翻译为 404。
- 小幅纠正：`session.delete(record)` 不是“自带包的简约写法”，而是 ORM 实例删除；条件 DELETE 则是 SQL 表达式删除，可按 where 条件影响 0 条或多条。
- 将 `2.3 不遮蔽数据库细节的 CRUD 写法` 标记为掌握，并安排 2026-05-12 复习。

### 2026-05-11：2.3 准备收尾

- 学习者询问是否可以结束 2.3。
- 当前已经完成 CRUD 五件套，并讨论了 `select/execute/scalar_one_or_none`、`session.get` 取舍、update/delete 前查询、ORM 删除与条件 DELETE 的差异。
- 结论：内容层面可以收尾；若要标记掌握，需要再完成 2-3 个简短自测问题。

### 2026-05-11：2.3 CRUD 复盘：为什么 update/delete 前先查询

- 学习者回答：先查询是为了确认数据库中存在记录；若不存在还提交，会因为空记录导致数据库报错。
- 纠正：确认存在是正确的；但查不到时通常没有 ORM 对象可更新/删除，也不会天然产生“空记录”。如果代码直接访问 `None.title` 会在 Python 层报错；如果执行按条件 UPDATE/DELETE，可能只是影响 0 行。
- 待继续：区分 Python 层 `None` 错误、ORM 对象更新、SQL UPDATE/DELETE 影响行数，以及 API 层应翻译成 404。

### 2026-05-11：2.3 CRUD 五件套完成

- 学习者已在 `practice.py` 中完成创建、查询单条、查询多条、更新、删除函数。
- 当前实现使用 `select(...).where(...)`、`session.execute(...).scalar_one_or_none()`、`session.scalars(...).all()`、`session.add()`、`session.delete()` 与 `session.commit()`。
- 待收尾：运行完整 CRUD 流程，观察 INSERT/SELECT/UPDATE/DELETE SQL；讨论 update/delete 后是否需要 `refresh`、是否返回 detached ORM 对象，以及何时使用 `session.get()` 简化主键查询。

### 2026-05-11：2.3 CRUD 练习：stmt 写法与 execute/scalar_one_or_none

- 学习者基本完成 `get_record` 与 `update_record`，使用 `select(...)` 构造 stmt，并通过 `session.execute(stmt).scalar_one_or_none()` 查询。
- 反馈：这种写法能显式暴露查询条件、执行位置和提交位置，符合“不遮蔽数据库细节”的训练目标。
- 纠正：`execute(stmt)` 返回的是 `Result`；只有继续 `.all()` 才会得到 Row 列表，`scalar_one_or_none()` 会直接从结果中取第一列并要求 0 或 1 条。

### 2026-05-11：开始 2.3 不遮蔽数据库细节的 CRUD 写法

- 从 2.2 的 `engine/session/model/select` 练习推进到 2.3 CRUD。
- 本节目标：写创建、读取、更新、删除函数时，不把数据库行为藏成“魔法”，而是明确 session、查询、提交、刷新、找不到、冲突和事务边界。
- 下一步围绕 `LearningRecord` 写 `create_record`、`get_record`、`list_records`、`update_record`、`delete_record`。

### 2026-05-10：2.2 完成查询多条练习并追问 order_by

- 学习者完成 `list_records()`，使用 `select(LearningRecord)`、`session.scalars(stmt).all()` 查询全部 ORM 对象。
- 追问是否应该加入 `order_by`；反馈重点：查询多条时如果结果顺序有业务含义，应显式排序，否则数据库不保证稳定顺序。
- 待继续：在 `list_records()` 中尝试 `order_by(LearningRecord.id)` 与 `order_by(LearningRecord.created_at.desc())`，观察 SQL 和输出顺序。

### 2026-05-10：整理 2.2 追问笔记

- 新增笔记 [[06-sqlalchemy-core-concepts]]，专门整理本节追问而非泛泛罗列 API。
- 覆盖内容：SQLite 与 SQLAlchemy 的边界、`create_engine` 连接配置、`Base.metadata`、`drop_all/create_all`、`Mapped/mapped_column`、默认时间、ORM 对象生命周期、`add/flush/commit/refresh`、`execute/scalar/scalars`。
- 后续可让学习者补写 `My Understanding`，验证是否能用自己的话解释 2.2。

### 2026-05-10：2.2 完成查询方法并辨析 scalar/scalars/execute

- 学习者完成 `query_record_by_title(title)`，使用 `select(LearningRecord).where(...)` 与 `session.scalar(stmt)` 查询单条记录。
- 纠正一个细节：`session.scalar(stmt)` 返回第一行第一列或 `None`，多条结果时不会自动抛错；需要唯一性校验时应使用 `scalar_one()` 或 `scalar_one_or_none()`。
- 待继续：区分 `execute()` 返回 Row 结果、`scalars()` 提取 ORM 对象序列、`.all()` 收集全部结果。

### 2026-05-10：2.2 完成重写练习 2：插入记录与 ORM 对象生命周期

- 学习者完成 `insert_record(title, content)`，使用 `Session(engine)`、`session.add()`、`session.commit()`、`session.refresh()` 插入学习记录。
- 主要问题转向 ORM 对象生命周期：`record` 在创建、加入 session、提交、刷新、session 关闭之后分别处于什么状态。
- 待继续：深入理解 transient、pending、persistent、detached，以及 `commit` 后对象属性过期与 `refresh` 的作用。

### 2026-05-10：2.2 完成重写练习 1：建表链路

- 学习者完成 `practice.py` 练习 1，并成功运行 SQLite 建表流程。
- 代码包含 `engine`、继承 `DeclarativeBase` 的 `Base`、`LearningRecord` model、`drop_all/create_all`。
- 主要问题集中在：为什么要声明 `Base`、如何设置默认当前时间、`mapped_column` 与旧式 `Column` 的区别。

### 2026-05-10：2.2 调整练习方式：从成品参考改为重写练习

- 学习者指出此前已经接触过 SQLAlchemy，本轮更适合自己练习，而不是直接阅读完整成品。
- 解释 `Base.metadata.drop_all(engine)` 与 `Base.metadata.create_all(engine)` 的用途：根据 model 元数据删除/创建表。
- 新增练习 [[../exercises/06-rewrite-sqlalchemy-basics]]，要求从空文件重写 engine、Base、model、建表、插入、查询和唯一约束错误观察。

### 2026-05-10：2.2 环境依赖：为 SQLAlchemy demo 补充 conda 配置

- 学习者发现 conda 环境可能没有安装 SQLAlchemy，导致无法识别 `sqlalchemy` 包。
- 确认当前 base Python 中已有 SQLAlchemy 2.0.49，但原 `environment.yml` 未声明该依赖。
- 已为 FastAPI demo 环境补充 `sqlalchemy`，并为 `02-sqlalchemy-sqlite-basics` 新增轻量 `environment.yml`。

### 2026-05-10：2.2 区分 SQLite、SQLAlchemy 与数据库连接配置

- 学习者追问 SQLite 是否是数据库软件、SQLAlchemy 是否是 Python 与数据库交互的语言，以及 demo 中数据库连接配置如何生效。
- 反馈：SQLite 是轻量嵌入式数据库；SQLAlchemy 不是数据库，也不是语言，而是 Python 数据库工具库/ORM；连接配置集中体现在 `create_engine("sqlite:///demo.db")` 的数据库 URL。
- 待继续：解释数据库 URL 的结构，并与后续 settings 中的 `DATABASE_URL` 连接起来。

### 2026-05-10：2.2 SQLite 最小练习 demo

- 新增练习 [[../exercises/05-sqlalchemy-sqlite-basics]]。
- 新增 demo `projects/demos/02-sqlalchemy-sqlite-basics`，使用 SQLite 和 SQLAlchemy 2.0 跑通 `engine -> model -> session -> select`。
- 已验证脚本能创建 `demo.db`，插入 `alice`，按 username 查询，并列出所有用户。

### 2026-05-10：正式开始 2.2 SQLAlchemy 2.0 核心概念

- 开始学习 `engine`、`session`、`model`、`query/select` 的心智模型。
- 本节目标：理解 SQLAlchemy 如何把 Python 代码和数据库操作连接起来，而不是先背 API。
- 暂不标记掌握；后续通过最小 SQLite demo 和 CRUD 练习验证。

### 2026-05-10：调整 2.1 学习策略，准备进入 2.2

- 学习者说明此前学过数据库和设计范式，2.1 当前不需要深入展开。
- 决定将 2.1 作为项目实践中的随用随复盘内容，不在此处做长时间理论停留。
- 下一步进入 2.2 SQLAlchemy 2.0 核心概念：engine、session、model、query。

### 2026-05-10：正式开始 2.1 关系型建模总览

- 进入第二章第一节：关系型建模，目标是理解如何把业务对象设计成数据库表。
- 本节总览内容包括：表、行、列、主键、外键、非空约束、唯一约束、检查约束和索引。
- 暂不标记掌握；后续通过学习记录智能体的表设计练习验证理解。

### 2026-05-10：2.1 唯一约束：username 不可重复

- 学习者回忆到唯一约束对应 `unique`，并判断 `username` 必须唯一。
- 反馈：方向正确；唯一约束表达的是“数据库层面不允许两行在某个字段或字段组合上重复”，常用于用户名、邮箱、第三方账号 ID、同一用户下不可重复的名称等。
- 待继续精炼：区分唯一约束、主键、非空约束和普通索引；理解唯一约束可以是单字段，也可以是组合字段。

### 2026-05-10：2.1 约束设计：非空约束与外键可空性

- 学习者判断主键、用户外键、创建时间、LLM model 等字段应为非空，并提出三张表大多数字段都可以全部非空。
- 反馈重点：主键天然非空；`user_id` 这类归属外键通常非空；但 `record_id` 是否非空取决于 LLM 调用是否一定绑定到某条学习记录。
- 待继续精炼：区分“数据库字段有值更整齐”和“业务规则要求它必须有值”；下一步补充唯一约束与索引设计。

### 2026-05-10：2.1 建模练习：学习记录智能体的最小表设计

- 学习者提出最少三张表：学习内容记录表、用户表、每个用户对于大模型的访问记录表。
- 反馈：这已经覆盖了核心业务数据、身份归属和 LLM 调用审计三个方向，适合作为第一版建模起点。
- 待继续精炼：区分“学习内容记录”是否需要拆成 session、note、concept、review；明确三张表之间的外键关系、唯一约束、非空约束和索引。

### 2026-05-09：开始第二章总览：数据库与 SQLAlchemy

- 读取当前进度后确认：第一章已覆盖到 1.5 配置管理的入口，但尚未将 1.x 概念标记为掌握。
- 第二章采用“地图优先”的方式进入：先建立关系型数据库、SQLAlchemy、CRUD、关系加载、迁移和事务的整体框架。
- 本次只记录进入第二章总览，不标记掌握概念，不新增间隔复习项。

### 2026-05-09：开始 1.5 配置管理、环境变量与应用 settings

- 总览配置管理的作用：让同一份代码适配本地、测试、生产等不同运行环境。
- 说明不应把数据库地址、密钥、日志级别、第三方 API key 等写死在代码中。
- 初步介绍环境变量是运行环境提供给程序的键值对，settings 是应用内部集中读取和校验配置的对象。
- 创建笔记 [[05-configuration-environment-settings]]。

### 2026-05-09：整理第一章问题复盘

- 新增总结 [[../summaries/01-module1-question-review]]，不重复已有知识点，专门整理学习过程中暴露出的疑问。
- 问题集中在：HTTPException 与普通 return、409 与 422、response_model、middleware 返回值契约、await/call_next、logging 配置、LogRecord 字段来源、`msg` 与 `args`。
- 特别记录一次教学偏差：解释 logging formatter 时应优先区分消息模板格式化和整条日志 formatter 格式化。

### 2026-05-09：纠正 logging 级别理解

- 澄清 `record.levelname` 不是由 `dictConfig` 中的 `"level"` 填充，而是由本次调用的日志方法决定，例如 `logger.info` 产生 `INFO`。
- 澄清 `"level": "INFO"` 是过滤门槛：决定 `INFO` 及以上日志是否允许通过。
- 反思教学偏差：前一次解释被消息模板 `"%s"` 带偏，重复解释了学习者已理解的按位置格式化，没有优先回答 formatter 如何按 `LogRecord` 字段名取值。

### 2026-05-09：澄清 dictConfig formatter 如何按字段名取值

- 学习者指出真正困惑点不是 `"%s"` 消息模板，而是 `dictConfig` 里的 `%(levelname)s`、`%(name)s` 如何找到对应值。
- 解释 formatter 会接收 logging 创建的 `LogRecord`，并通过类似 `fmt % record.__dict__` 的方式按字段名取值。
- 区分字段来源：`name` 来自 logger 名称，`levelname` 来自调用的日志级别，`message` 来自 `msg + args`，`pathname/lineno/funcName` 来自调用位置。

### 2026-05-09：澄清日志级别与 formatter 字段来源

- 解释 `%(levelname)s`、`%(name)s`、`%(message)s` 来自 logging 内部创建的 `LogRecord`，不是用户手动定义的普通变量。
- 区分日志级别：`DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL`。
- 说明 `"level": "INFO"` 表示允许 `INFO` 及以上级别输出，低于 `INFO` 的 `DEBUG` 不输出。
- 补充常见 formatter 字段：`asctime`、`pathname`、`lineno`、`funcName`。

### 2026-05-09：细讲 dictConfig 日志配置

- 将 `dictConfig` 拆成三层理解：formatter 决定日志长相，handler 决定输出位置，logger 决定哪些模块以什么级别输出。
- 解释日志调用链：`logger.info` -> logger 级别判断 -> handler -> formatter -> 输出。
- 补充 `version`、`disable_existing_loggers`、`propagate`、`app` logger、`httpx` logger 的含义到 1.4 笔记。

### 2026-05-09：从 basicConfig 过渡到 dictConfig

- 解释 `logging.basicConfig` 是快速默认配置，适合简单 demo，但不适合复杂项目精细控制。
- 将 demo 改为 `logging.config.dictConfig`，显式配置 formatter、console handler、`app` logger 和第三方 `httpx` logger。
- 验证日志输出只保留 `INFO:app.main:...`，`httpx` 的 INFO 级日志被压到 `WARNING` 以上。

### 2026-05-09：配置 logging 并观察日志输出

- 在 demo 中添加 `logging.basicConfig(level=logging.INFO)`，让 `logger.info` 输出到终端。
- 使用 `TestClient` 观察日志：`INFO:app.main:GET /health -> 200 in ...s`、`GET /users/2 -> 404`、`POST /users -> 409`。
- 观察到测试客户端 `httpx` 也会输出 INFO 日志，后续可学习按 logger 名称控制不同模块的日志级别。

### 2026-05-09：完成 1.4 logging 代码并追问 logger API

- 在计时中间件中添加 `logger.info`，记录 method、path、status_code、duration。
- 深入讨论 `logging.getLogger(__name__)` 的参数含义：logger 名称通常用模块名，便于按模块管理日志。
- 深入讨论日志格式字符串 `%s %s -> %s in %.4fs`：使用占位符延迟格式化日志参数。
- 澄清 `info` 是日志级别之一，日志输出位置由 handler 决定，可能是控制台、文件或外部日志系统。

### 2026-05-09：继续 1.4 logging 学习

- 暂时搁置线程池细节，保留为后续“同步代码与异步服务”专题。
- 进入 logging：理解日志是服务端排查用的运行记录，不是给客户端展示的响应内容。
- 下一步练习：在计时中间件中记录 method、path、status_code、duration，且不记录请求体中的 password/token 等敏感信息。

### 2026-05-09：完成 1.4 计时中间件并追问返回值契约

- 在 demo 中添加 `@app.middleware("http")` 计时中间件。
- 验证 `200`、`404`、`409` 响应都带有 `X-Process-Time` header。
- 深入讨论 middleware 的返回值契约：中间件最终必须返回一个 Response 类对象；可以返回 `call_next(request)` 得到的响应，也可以提前返回自定义响应。
- 待继续：添加基础 logging，记录 method、path、status_code、duration。

### 2026-05-09：完成 1.4 第一轮代码练习

- 在 demo 中为 `GET /users/{user_id}` 添加 `404 User not found`。
- 在 `POST /users` 中为 `username == "alice"` 添加 `409 Username already exists`。
- 使用 `TestClient` 验证：正常查询返回 `200`，不存在用户返回 `404`，用户名冲突返回 `409`，schema 校验失败仍返回 `422`。
- 下一步：补充 middleware，请求耗时 header 和基础请求日志。

### 2026-05-08：1.4 深度问答反馈

- 学习者能够区分 `422` 表示请求体可解析但未通过 schema，`409` 表示请求与当前资源状态冲突。
- 学习者初步理解 `HTTPException` 的价值：不是正常返回，而是让 HTTP 层产生正确状态码和错误响应。
- 学习者能够说明 middleware 包裹每个请求，可用于计时、分配 request id 等统一处理。
- 待精炼表达：`HTTPException` 不是“让机器报错”，而是把业务失败翻译成符合 HTTP 语义的响应；logging 记录服务端运行事实，不等同于给客户端返回错误。

### 2026-05-08：深入 1.4 错误响应设计与可观测性

- 深入拆解 API 错误设计的三层：HTTP 状态码、错误响应体、服务端日志。
- 区分 `400`、`404`、`409`、`422` 的适用边界。
- 说明 `HTTPException` 更适合位于 HTTP 层，真实项目中可以把 service 的业务异常翻译成 API 响应。
- 区分 middleware、exception handler、logging 的职责。
- 新增练习 [[../exercises/04-error-status-middleware-logging]]，用于实践 404、409、请求耗时中间件和基础日志。

### 2026-05-08：开始 1.4 错误处理、状态码、中间件与日志

- 总览状态码的语义：`2xx` 成功、`4xx` 客户端问题、`5xx` 服务端问题。
- 说明 `HTTPException` 用于把业务错误转换成明确的 API 错误响应。
- 初步介绍中间件在请求进入 endpoint 前后包裹请求生命周期。
- 初步介绍日志的作用：记录运行过程、错误、慢请求和关键业务事件。
- 创建笔记 [[04-error-status-middleware-logging]]。

### 2026-05-08：开始 1.3 Pydantic schema、数据校验、序列化与响应模型

- 总览 schema 在 FastAPI 中的作用：描述请求和响应的数据结构。
- 区分请求 schema 与响应 schema：前者校验外部输入，后者约束对外输出。
- 说明校验发生在 endpoint 之前，序列化发生在 endpoint 返回之后。
- 创建笔记 [[03-pydantic-validation-serialization]]。

### 2026-05-08：扩展 1.3 Pydantic 深入点

- 补充字段约束、默认值、可选字段、嵌套模型、自定义字段校验和跨字段校验。
- 说明 422 错误结构如何阅读：重点看 `loc`、`type`、`msg`。
- 新增练习 [[../exercises/03-pydantic-validation-serialization]]，用于实践 `Field()`、`field_validator()` 和 `response_model`。

### 2026-05-08：完成 1.3 复盘

- 学习者能够说明：字符串长度、列表长度、数值范围等单字段规则适合用 `Field()`。
- 学习者能够说明：空格检测、开头约束等 `Field()` 不易表达的规则适合用 `field_validator()`。
- 学习者能够说明：`response_model` 可以过滤不在响应模型中的字段，例如 `password_hash`。
- 待精炼表达：`Field()` 约束的是 schema 字段；`response_model` 不只是返回类型标注，还参与响应校验、序列化和字段过滤。

### 2026-05-07：快速过 1.2 路由函数、依赖注入与应用结构

- 总览路由函数如何把 HTTP 方法 + URL 路径绑定到 Python 函数。
- 说明 FastAPI 如何通过函数参数判断路径参数、查询参数、请求体和依赖。
- 初步介绍 `Depends()` 的用途：把数据库 session、当前用户、配置、业务服务等公共对象注入到接口函数中。
- 创建笔记 [[02-path-operations-dependencies-structure]]。

### 2026-05-07：学习 1.1 POST 请求体与 Pydantic 校验流程

- 阅读并讨论 `Demo 01` 中的 `POST /echo` 实现。
- 当前理解：POST 路由接收请求体，并按照 Pydantic 模型进行校验。
- 待巩固：FastAPI 如何根据函数参数位置和类型标注判断数据来源，以及 422 错误是如何产生的。

### 2026-05-07：初始化学习项目

- 创建 `fastapi + agent` 学习 vault。
- 搭建从后端基础到 Obsidian 学习记录智能体的分阶段路线。
- 下一次从 [[01-http-asgi-fastapi-lifecycle]] 和一个最小 FastAPI demo 开始。
<!-- BLOOM:SESSION_LOG:END -->
