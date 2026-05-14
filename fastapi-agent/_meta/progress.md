# 学习进度：FastAPI + Agent

## 当前状态
<!-- BLOOM:CURRENT_STATE:START -->
- **Current module**: ?? 2????? SQLAlchemy
- **Current concept**: 2.6 ??????????
- **Overall mastery**: 2/5 concepts mastered
- **Session count**: 46
- **Last session**: 2026-05-13
- **Learner level**: intermediate
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
### Session 46 - 2026-05-13
- Summary: ?? 2.6b ?????????????????????? FastAPI ?? demo??? app/ ???? db.py?models.py?schemas.py?exceptions.py?services/users.py?api/users.py ? main.py??? engine ?? sqlite+aiosqlite?session ?? Depends ???User.name ???????????? create_user service ?????????API ?????? UserNameConflictError ???? 409 Conflict?
- Module: ?? 2????? SQLAlchemy
- Concept: 2.6 ??????????
- Covered concepts: ?? FastAPI + SQLAlchemy demo ?????, AsyncSession ????, ???????? API 409 ?????
- Struggles: ?? Python ???? aiosqlite??? app ??????????; create_user service ??????????????
- Wins: ???? FastAPI app ??; ?????????????? create_user ????; ?? py_compile ????
- Next session: ?? app/services/users.py ?? async create_user?add?commit?refresh??? IntegrityError ? rollback ? raise UserNameConflictError????? FastAPI???? POST /users ??????? 409?

### Session 45 - 2026-05-13
- Summary: ???? 2.6b ??????????? lost update ?????? UPDATE ???????? concurrency_examples.py??? LearningRecord ?? view_count ??????? session ???? view_count=0 ????? +1????????? 1?????? session ??????????????? SQLAlchemy update(...).values(view_count=LearningRecord.view_count + 1) ? +1 ???????????????????? 2????????? UPDATE ????????
- Module: ?? 2????? SQLAlchemy
- Concept: 2.6 ??????????
- Covered concepts: lost update ????????, Python ?????-?-??????? UPDATE ???, ???? Session ??????
- Struggles: ??????? IntegrityError -> 409 ??????; 2.6 ??????????????????
- Wins: ????? concurrency_examples.py; ????? ORM ?????? view_count=1; ??????? view_count = view_count + 1 ?? view_count=2
- Next session: ?? 2.6b?? User.name ????????????????????????? IntegrityError??????? FastAPI ???? 409 Conflict?

### Session 44 - 2026-05-12
- Summary: 开始学习 2.6 事务、并发与失败边界。本次重点完成事务与失败边界部分：理解 commit 是事务结束并确认成功的标志，flush 会发送 SQL 并可拿到数据库生成的 id，但不会结束事务；rollback 可以撤销同一事务中尚未提交的 flush 操作。通过新建 demos/04-transaction-boundaries 练习，观察提前 commit 会留下半完成状态，flush + rollback 可以保持原子性，with session.begin() 可以自动提交或回滚。完成 tasks.py 三个实践任务并通过 check_tasks.py，能处理 user + default record 的原子创建、NOT NULL 失败回滚、外键失败回滚。已意识到 2.6 的并发部分尚未学习，需要继续 2.6b。
- Module: 模块 2：数据库与 SQLAlchemy
- Concept: 2.6 事务、并发与失败边界
- Covered concepts: 事务边界与业务成功/失败边界, flush 与 commit 的区别, rollback 撤销未提交事务, 提前 commit 会破坏原子性, with session.begin() 自动管理事务, IntegrityError 与失败回滚, 并发部分待继续：lost update、原子 UPDATE、唯一约束冲突
- Struggles: 并发控制尚未展开学习，2.6 暂不标记为完全掌握; 需要继续通过 lost update 和冲突处理实验建立并发直觉
- Wins: 创建并运行 demos/04-transaction-boundaries 事务练习 demo; 能解释 Alice 留下、Bob 消失的原因; 完成 tasks.py 三个事务实践任务; check_tasks.py 三项全部通过; 明确 2.6 需要拆成事务失败边界和并发边界两部分
- Next session: 继续 2.6b 并发与冲突边界：新增 concurrency_examples.py，演示 lost update、数据库原子 UPDATE、唯一约束冲突与 IntegrityError -> 409 的处理思路。

### Session 43 - 2026-05-12
- Summary: 继续学习 2.5 Alembic 迁移：明确 Alembic 的作用是管理数据库 DDL 变更历史，而不是替代 ORM models；理解 env.py 主要负责把 Alembic 和 SQLAlchemy 的 Base.metadata 接起来。通过在 models.py 中新增 avatar_url 字段，先执行已有 001/002 迁移创建本地 SQLite 数据库，再使用 autogenerate 生成第三个 version，并执行 upgrade head 将数据库更新到最新结构。随后查看 alembic_version 表和 users 表结构，确认 avatar_url 已进入数据库；理解 upgrade head 会从 alembic_version 记录的当前 revision 一路升级到 head，downgrade -1 表示从当前 revision 回退一步。
- Module: 模块 2：数据库与 SQLAlchemy
- Concept: 2.5 Alembic 迁移与数据库结构演进
- Covered concepts: Alembic 的作用：管理数据库结构演进历史, alembic_version 表记录当前数据库 revision, upgrade head 从当前 revision 升级到最新 head, downgrade -1 回退一个 revision, autogenerate 生成迁移草稿后需要人工审阅, SQLite 表结构检查：sqlite_master 与 pragma table_info
- Struggles: env.py 作为框架胶水代码仍然偏抽象，暂时不要求复写，只保留关键识别点; 对 migration 文件的学习目标已从手写调整为审阅 Alembic 自动生成的草稿
- Wins: 成功生成并执行第三个 migration：add user avatar_url; 能解释本地没有 db 时 Alembic 会从 base 依次执行 001、002、003; 能说明 online 模式会真实连接数据库执行迁移; 能通过数据库结构确认 migration 是否生效
- Next session: 做一次 2.5 小自测：解释 models、versions、env.py、alembic.ini、alembic_version 各自职责；再练习 downgrade -1 后检查 avatar_url 消失，upgrade head 后检查它恢复。

### Session ? - 2026-05-11
- Summary: 2.4 掌握度自测通过：学习者能解释 selectinload 的两次查询与外键归档、relationship append 后 Python 对象层双向绑定以及 flush/commit 时外键同步，也能对比 lazy/selectinload/joinedload 的 SQL 次数和对象装配。小纠正：100 个 user、每人约 3 条 records 时，lazy loading 是 1 + 100 = 101 次 SQL，不是 301 次；300 更接近 records 结果行数量。
- Module: N/A
- Concept: N/A
- Mastered: 2.4 表关系、懒加载/预加载与 N+1 问题
- Next session: 进入 2.5 Alembic 迁移与数据库结构演进；2026-05-12 复习 2.3 和 2.4。

### Session ? - 2026-05-11
- Summary: 2.4 拆分练习代码并增加预加载对比：将 practice.py 拆分为 db.py、models.py、crud.py、loading_examples.py 和入口 practice.py；新增 list_users_lazy、list_users_with_selectinload、list_users_with_joinedload，用于对比懒加载、批量预加载和 JOIN 风格预加载。新增 exercises/07-relationships-loading-n-plus-one.md；已运行验证三种加载方式，观察到懒加载多次 SELECT records，selectinload 使用 WHERE user_id IN (...)，joinedload 使用 JOIN 并需要 unique。
- Module: N/A
- Concept: N/A
- Next session: 让学习者重点练习 selectinload(User.records) 参数含义，并解释 joinedload 为什么需要 unique。

### Session ? - 2026-05-11
- Summary: 2.4 创建 User 与多条 LearningRecord：在 practice.py 中补充 create_user(name) 与 create_user_with_records(name, records_data)，并调整 insert_record 需要显式传入 user_id 以满足非空外键约束。已运行验证：创建 alice 后插入一条记录；创建 bob 时通过 user.records.append(...) 关联两条记录，并观察到访问 user.records 会触发关系查询。
- Module: N/A
- Concept: N/A
- Next session: 继续观察懒加载：查询多个 User 后循环访问 user.records，制造并解释 N+1 问题。

### Session ? - 2026-05-11
- Summary: 2.4 relationship 与 back_populates：学习者已添加 User 表并将其与 LearningRecord 关联，追问 relationship 是否是表中的列，以及 back_populates 的作用。反馈 ForeignKey 是数据库列，relationship 不是表列，而是 ORM 层对象导航属性；back_populates 声明两边关系互相对应，保持 user.records 与 record.user 的双向同步。待修正类名用 User，不需要 users.record_ids。
- Module: N/A
- Concept: N/A
- Next session: 修改 User/LearningRecord 关系模型，并通过创建 user.records append record 的方式观察 user_id 如何自动同步。

### Session ? - 2026-05-11
- Summary: 开始 2.4 表关系、懒加载/预加载与 N+1 问题：从单表 CRUD 进入多表关系查询，目标是理解一对多、多对一、多对多关系如何在 SQLAlchemy 中表达，以及懒加载、预加载和 N+1 问题的取舍。
- Module: N/A
- Concept: N/A
- Next session: 围绕学习记录系统设计 User -> LearningRecord 或 LearningRecord -> Note 的关系 demo。

### Session ? - 2026-05-11
- Summary: 2.3 掌握度自测通过：学习者能说明 update 前先查询是为了确认记录存在并返回真实错误原因；能区分 ORM 对象删除与条件 DELETE；能说明 None/False 在 FastAPI 层通常翻译为 404。纠正 session.delete(record) 是 ORM 实例删除，不是简单包函数；条件 DELETE 是 SQL 表达式删除，可影响 0 条或多条。
- Module: N/A
- Concept: N/A
- Mastered: 2.3 不遮蔽数据库细节的 CRUD 写法
- Next session: 进入 2.4 表关系、懒加载/预加载与 N+1 问题；2026-05-12 复习 2.3。

### Session ? - 2026-05-11
- Summary: 2.3 准备收尾：学习者询问是否可以结束本节。当前已经完成 CRUD 五件套，并讨论 select/execute/scalar_one_or_none、session.get 取舍、update/delete 前查询、ORM 删除与条件 DELETE 的差异。内容层面可以收尾；若要标记掌握，需要完成 2-3 个简短自测问题。
- Module: N/A
- Concept: N/A
- Next session: 进行 2.3 掌握度自测；通过后将 2.3 加入间隔复习，否则针对薄弱点补一轮。

### Session ? - 2026-05-11
- Summary: 2.3 CRUD 复盘：学习者回答 update/delete 前先查询是为了确认记录存在；若不存在还提交，会因为空记录导致数据库报错。反馈确认存在是正确的，但查不到时通常没有 ORM 对象可更新/删除，不会天然产生空记录；直接访问 None.title 会在 Python 层报错，按条件 UPDATE/DELETE 则可能只是影响 0 行。API 层应把不存在翻译成 404。
- Module: N/A
- Concept: N/A
- Next session: 继续复盘 update 后是否需要 refresh、返回 detached ORM 对象的边界，以及 session.get 与 select 的取舍。

### Session ? - 2026-05-11
- Summary: 2.3 CRUD 五件套完成：学习者已在 practice.py 中完成创建、查询单条、查询多条、更新、删除函数。当前实现使用 select/where、execute.scalar_one_or_none、scalars.all、add、delete、commit。下一步收尾是运行完整 CRUD 流程，观察 INSERT/SELECT/UPDATE/DELETE SQL，并讨论 update/delete 后是否需要 refresh、返回 detached ORM 对象的边界，以及何时用 session.get 简化主键查询。
- Module: N/A
- Concept: N/A
- Next session: 运行完整 CRUD 流程并做 2.3 小复盘，确认是否可以把 2.3 标记为进入间隔复习。

### Session ? - 2026-05-11
- Summary: 2.3 CRUD 练习：学习者基本完成 get_record 与 update_record，使用 select(...) 构造 stmt，并通过 session.execute(stmt).scalar_one_or_none() 查询。反馈这种写法能显式暴露查询条件、执行位置和提交位置，符合不遮蔽数据库细节的训练目标；纠正 execute(stmt) 返回 Result，不是直接的元组列表，只有 .all() 后才得到 Row 列表。
- Module: N/A
- Concept: N/A
- Next session: 继续补 delete_record，并讨论 update 后是否需要 refresh、返回 detached ORM 对象的边界，以及 session.get 与 select 写法的取舍。

### Session ? - 2026-05-11
- Summary: 开始 2.3 不遮蔽数据库细节的 CRUD 写法：从 2.2 的 engine/session/model/select 练习推进到 create/read/update/delete，目标是在写 CRUD 函数时明确 session、查询、提交、刷新、找不到、冲突和事务边界，而不是把数据库行为藏成魔法。
- Module: N/A
- Concept: N/A
- Next session: 围绕 LearningRecord 写 create_record、get_record、list_records、update_record、delete_record，并观察每一步产生的 SQL。

### Session ? - 2026-05-10
- Summary: 2.2 完成查询多条练习：学习者完成 list_records()，使用 select(LearningRecord) 与 session.scalars(stmt).all() 查询全部 ORM 对象；追问是否应该加入 order_by。反馈重点是查询多条时如果顺序有业务含义，应显式 order_by，否则数据库不保证稳定顺序。
- Module: N/A
- Concept: N/A
- Next session: 让学习者在 list_records 中分别尝试 order_by(LearningRecord.id) 与 order_by(LearningRecord.created_at.desc())，观察 SQL 和结果顺序。

### Session ? - 2026-05-10
- Summary: 整理 2.2 追问笔记：新增 notes/06-sqlalchemy-core-concepts.md，重点整理 SQLite 与 SQLAlchemy 的边界、create_engine 连接配置、Base.metadata、drop_all/create_all、Mapped/mapped_column、默认时间、ORM 对象生命周期、add/flush/commit/refresh、execute/scalar/scalars 等学习者追问内容。
- Module: N/A
- Concept: N/A
- Next session: 让学习者补写 06 笔记中的 My Understanding，并继续完成 list_records 查询多条记录练习。

### Session ? - 2026-05-10
- Summary: 2.2 完成查询方法并辨析查询 API：学习者完成 query_record_by_title(title)，使用 select(LearningRecord).where(...) 与 session.scalar(stmt) 查询单条记录。纠正 scalar 行为：它返回第一行第一列或 None，多条结果时不会自动抛错；需要唯一性校验时使用 scalar_one 或 scalar_one_or_none。下一步区分 execute 返回 Row、scalars 提取 ORM 对象序列、all 收集全部结果。
- Module: N/A
- Concept: N/A
- Next session: 继续完成 list_records，并用 execute/scalars/scalar_one_or_none 对同一个查询做对比实验。

### Session ? - 2026-05-10
- Summary: 2.2 完成重写练习 2：学习者完成 insert_record(title, content)，使用 Session(engine)、session.add、session.commit、session.refresh 插入学习记录。问题转向 ORM 对象生命周期：record 在创建、加入 session、提交、刷新、session 关闭后分别处于什么状态，以及提交后对象是否还能使用。
- Module: N/A
- Concept: N/A
- Next session: 继续解释 transient、pending、persistent、detached 状态，并通过在 session 内外访问 record.id/title/created_at 观察对象行为。

### Session ? - 2026-05-10
- Summary: 2.2 完成重写练习 1：学习者完成 practice.py 的 SQLite 建表链路，包含 engine、DeclarativeBase、LearningRecord model、drop_all/create_all；主要问题集中在为什么要声明 Base、如何设置默认当前时间、mapped_column 与 Column 的区别。
- Module: N/A
- Concept: N/A
- Next session: 继续练习 2：插入 LearningRecord，并解释 session.add、commit、refresh 和默认时间生成发生在何时。

### Session ? - 2026-05-10
- Summary: 2.2 调整练习方式：学习者指出此前已经接触过 SQLAlchemy，本轮更适合自己练习，而不是直接阅读完整成品。解释 Base.metadata.drop_all(engine) 与 create_all(engine) 的用途，并新增 exercises/06-rewrite-sqlalchemy-basics.md，要求从空文件重写 engine、Base、model、建表、插入、查询和唯一约束错误观察。
- Module: N/A
- Concept: N/A
- Next session: 让学习者完成 practice.py 的练习 1-2，再根据代码讨论 metadata、create_all、drop_all、commit 和 refresh。

### Session ? - 2026-05-10
- Summary: 2.2 环境依赖处理：学习者发现 conda 环境可能没有安装 SQLAlchemy。确认当前 base Python 有 SQLAlchemy 2.0.49，但原 demo environment.yml 未声明 sqlalchemy；已为 FastAPI demo 环境补充 sqlalchemy，并为 02-sqlalchemy-sqlite-basics 新增轻量 environment.yml。
- Module: N/A
- Concept: N/A
- Next session: 继续运行 SQLAlchemy demo，并解释 conda env update/install 与 Python 解释器选择的关系。

### Session ? - 2026-05-10
- Summary: 2.2 概念澄清：学习者追问 SQLite 是否是数据库软件、SQLAlchemy 是否是 Python 与数据库交互的语言，以及 demo 中数据库连接配置如何生效。反馈 SQLite 是轻量嵌入式数据库，SQLAlchemy 是 Python 数据库工具库/ORM，连接配置集中体现在 create_engine("sqlite:///demo.db") 的数据库 URL。
- Module: N/A
- Concept: N/A
- Next session: 继续解释数据库 URL 结构，并把硬编码的 sqlite:///demo.db 过渡到 settings 中的 DATABASE_URL。

### Session ? - 2026-05-10
- Summary: 2.2 SQLite 最小练习 demo：新增 exercises/05-sqlalchemy-sqlite-basics.md 和 projects/demos/02-sqlalchemy-sqlite-basics，使用 SQLite 与 SQLAlchemy 2.0 跑通 engine -> model -> session -> select；已验证脚本能创建 demo.db、插入 alice、按 username 查询并列出所有用户。
- Module: N/A
- Concept: N/A
- Next session: 让学习者阅读 main.py 并解释 create_engine、Base.metadata.create_all、Session、session.add/commit/refresh、select/session.scalar 的职责。

### Session ? - 2026-05-10
- Summary: 正式开始 2.2 SQLAlchemy 2.0 核心概念：准备建立 engine、session、model、query/select 的心智模型，目标是理解 SQLAlchemy 如何把 Python 代码和数据库操作连接起来；暂不标记掌握，后续通过最小 SQLite demo 和 CRUD 练习验证。
- Module: N/A
- Concept: N/A
- Next session: 用一个最小 SQLite demo 创建 User model，完成建表、插入、查询，并观察 session.add/commit/refresh/select 的作用。

### Session ? - 2026-05-10
- Summary: 调整 2.1 学习策略：学习者此前学过数据库和设计范式，当前不需要深入理论展开；决定将 2.1 作为项目实践中的随用随复盘内容，下一步进入 SQLAlchemy 2.0 核心概念。
- Module: N/A
- Concept: N/A
- Next session: 进入 2.2：建立 engine、session、model、query/select 的心智模型，并用最小 demo 连接 SQLite。

### Session ? - 2026-05-10
- Summary: 正式开始 2.1 关系型建模总览：讲解如何把业务对象设计成数据库表，覆盖表、行、列、主键、外键、非空约束、唯一约束、检查约束和索引；暂不标记掌握，后续通过学习记录智能体的表设计练习验证。
- Module: N/A
- Concept: N/A
- Next session: 围绕学习记录智能体设计第一版 users、learning_records、llm_access_logs 表结构，并解释每个主键、外键、约束和索引的理由。

### Session ? - 2026-05-10
- Summary: 2.1 唯一约束学习：学习者回忆到 unique，并判断 username 必须唯一。反馈其方向正确，唯一约束表示数据库层面不允许两行在某个字段或字段组合上重复；下一步区分唯一约束、主键、非空约束和普通索引。
- Module: N/A
- Concept: N/A
- Next session: 继续 2.1：用 users、learning_records、llm_access_logs 分别判断哪些字段适合单字段唯一、哪些适合组合唯一、哪些只需要普通索引。

### Session ? - 2026-05-10
- Summary: 2.1 约束设计练习：学习者判断主键、用户外键、创建时间、LLM model 等字段应为非空，并提出三张表大多数字段都可以全部非空。反馈重点是区分技术上可以非空与业务上必须非空，尤其是 llm_access_logs.record_id 是否可空取决于一次 LLM 调用是否一定绑定到某条学习记录。
- Module: N/A
- Concept: N/A
- Next session: 继续 2.1：在三张表上补充唯一约束与索引设计，例如 users.email/username 唯一、按 user_id + created_at 查询的索引。

### Session ? - 2026-05-10
- Summary: 2.1 建模练习：学习者提出学习内容记录表、用户表、每个用户对于大模型的访问记录表。反馈其覆盖了核心业务数据、身份归属和 LLM 调用审计三个方向，下一步需要细化表之间的外键关系、约束、索引，并判断学习内容是否需要拆分为 session、note、concept、review。
- Module: N/A
- Concept: N/A
- Next session: 继续 2.1：为三张表补充主键、外键、唯一约束、非空约束和常用查询索引。

### Session ? - 2026-05-09
- Summary: 开始第二章总览：读取进度后确认第一章已覆盖到 1.5 入口但尚未标记掌握；用地图优先方式总览数据库与 SQLAlchemy，包括关系型建模、engine/session/model/query、CRUD、关系加载、Alembic 迁移和事务边界。
- Module: N/A
- Concept: N/A
- Next session: 进入 2.1：用学习记录智能体的领域对象建模表、主键、外键、唯一约束、非空约束和索引。

### Session ? - 2026-05-09
- Summary: 开始 1.5 配置管理：理解配置与代码分离、环境变量、settings 对象，以及它和日志、数据库、Agent API key 的关系。
- Module: N/A
- Concept: N/A
- Next session: 用 demo 实践 settings：把 LOG_LEVEL、APP_ENV 等从配置对象读取。

### Session ? - 2026-05-09
- Summary: 整理第一章问题复盘：汇总 HTTPException、状态码边界、response_model、middleware、await/call_next、logging、LogRecord、msg/args 等学习中暴露出的疑问。
- Module: N/A
- Concept: N/A
- Next session: 围绕第一章问题复盘做一次掌握度自测，并决定 1.4 是否进入间隔复习。

### Session ? - 2026-05-09
- Summary: 纠正 logging 级别理解：record.levelname 由 logger.info/warning/error 这次调用决定，dictConfig 的 level 是过滤门槛；同时反思前一次解释没有准确定位学习者卡点。
- Module: N/A
- Concept: N/A
- Next session: 继续用最小例子区分日志事件的字段生成、logger 级别过滤和 formatter 输出。

### Session ? - 2026-05-09
- Summary: 进一步澄清 dictConfig formatter 的取值机制：formatter 按字段名从 LogRecord 属性字典中取值，message 则由 msg 和 args 计算得到。
- Module: N/A
- Concept: N/A
- Next session: 用一个具体 LogRecord 例子复盘 dictConfig format 与 logger.info 消息模板的两层格式化。

### Session ? - 2026-05-09
- Summary: 澄清 logging formatter 字段来源：levelname、name、message 等来自 LogRecord；理解 INFO 级别会输出 INFO 及以上日志。
- Module: N/A
- Concept: N/A
- Next session: 用自测题复盘 logging：formatter 字段、日志级别、logger 名称匹配。

### Session ? - 2026-05-09
- Summary: 细讲 dictConfig：理解 formatter、handler、logger 的分工，以及 propagate、app logger、httpx logger 的作用。
- Module: N/A
- Concept: N/A
- Next session: 用一个小自测确认是否掌握 logging 配置的基本心智模型。

### Session ? - 2026-05-09
- Summary: 将 logging.basicConfig 升级为 dictConfig：显式配置 console handler、formatter、app logger，并把 httpx INFO 日志压到 WARNING。
- Module: N/A
- Concept: N/A
- Next session: 复盘 1.4：状态码、HTTPException、中间件、日志配置，并决定是否标记 1.4 掌握。

### Session ? - 2026-05-09
- Summary: 配置 logging.basicConfig(level=logging.INFO)，并通过 TestClient 观察到 app.main 的请求日志输出。
- Module: N/A
- Concept: N/A
- Next session: 复盘 logging 输出格式，理解 logger 名称、级别和第三方库日志的关系。

### Session ? - 2026-05-09
- Summary: 完成 1.4 logging 代码：在 middleware 中记录请求方法、路径、状态码和耗时；讨论 getLogger、日志格式字符串、info 级别和 handler 输出位置。
- Module: N/A
- Concept: N/A
- Next session: 用自测题复盘 1.4，并决定是否将 1.4 标记为掌握。

### Session ? - 2026-05-09
- Summary: 继续 1.4 logging 学习：将线程池细节延后，聚焦日志作为服务端排查记录的作用。
- Module: N/A
- Concept: N/A
- Next session: 在中间件中加入 logger.info，记录 method、path、status_code、duration。

### Session ? - 2026-05-09
- Summary: 完成 1.4 计时中间件：添加 X-Process-Time header，并验证成功和错误响应都会经过中间件；讨论 middleware 必须返回 Response 对象的契约。
- Module: N/A
- Concept: N/A
- Next session: 添加基础 logging，并理解中间件提前返回 Response 与继续 call_next 的区别。

### Session ? - 2026-05-09
- Summary: 完成 1.4 第一轮代码练习：GET /users/{user_id} 支持 404，POST /users 支持 username 冲突 409，并验证 schema 错误仍为 422。
- Module: N/A
- Concept: N/A
- Next session: 补充 middleware：添加 X-Process-Time 响应头，并记录 method、path、status_code、duration 的基础访问日志。

### Session ? - 2026-05-08
- Summary: 完成 1.4 深度问答反馈：已能区分 422 与 409，初步理解 HTTPException、middleware、logging 的职责；需要继续精炼 HTTPException 是错误响应翻译而非普通返回。
- Module: N/A
- Concept: N/A
- Next session: 进入 1.4 代码练习：改造 demo 中的 /users 接口，加入 404、409、X-Process-Time 和基础请求日志。

### Session ? - 2026-05-08
- Summary: 深入 1.4：错误响应设计、状态码边界、HTTPException 分层位置、中间件与日志职责。
- Module: N/A
- Concept: N/A
- Next session: 完成 1.4 练习：给 demo 添加 404、409、请求耗时中间件和基础日志，然后用自测问题验证掌握度。

### Session ? - 2026-05-07
- Summary: 初始化 FastAPI + Agent 学习项目，创建系统路线图、项目里程碑、第一篇概念笔记和第一个 demo 练习。
- Module: N/A
- Concept: N/A
- Next session: 通过一个最小 FastAPI API demo 学习 HTTP、ASGI 与 FastAPI 请求生命周期。
<!-- BLOOM:SESSION_LOG:END -->
