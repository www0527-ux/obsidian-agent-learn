# 知识地图：FastAPI + Agent

## 总览

这是一条从“接触过 FastAPI 和 Agent”走向“能独立设计、开发、调试、扩展后端 Agent 应用”的学习路线。最终目标是做出一个智能体：它能记录学习过程，把记录关联到 Obsidian 笔记，查询历史学习内容，并辅助安排复习和下一个 demo。

## 模块

### 模块 1：后端开发的基本心智模型
- [ ] 1.1 HTTP、ASGI 与 FastAPI 请求生命周期
- [ ] 1.2 路由函数、依赖注入与应用结构
- [ ] 1.3 Pydantic schema、数据校验、序列化与响应模型
- [ ] 1.4 错误处理、状态码、中间件与日志
- [ ] 1.5 配置管理、环境变量与应用 settings

### 模块 2：数据库与 SQLAlchemy
- [ ] 2.1 关系型建模：表、主键、外键、约束、索引
- [ ] 2.2 SQLAlchemy 2.0 核心概念：engine、session、model、query
- [x] 2.3 不遮蔽数据库细节的 CRUD 写法
- [x] 2.4 表关系、懒加载/预加载与 N+1 问题
- [ ] 2.5 Alembic 迁移与数据库结构演进
- [ ] 2.6 事务、并发与失败边界

### 模块 3：FastAPI 应用架构
- [ ] 3.1 分层结构：router、service、repository、schema、model
- [ ] 3.2 用依赖注入管理数据库 session 和业务服务
- [ ] 3.3 鉴权基础：用户、密码哈希、JWT/session 取舍
- [ ] 3.4 FastAPI 测试：单元测试、集成测试、测试数据库
- [ ] 3.5 后台任务、队列与长耗时任务
- [ ] 3.6 API 设计：分页、过滤、幂等性、版本管理

### 模块 4：Agent 基础
- [ ] 4.1 LLM 应用循环：prompt、state、tool call、observation、answer
- [ ] 4.2 三种 Agent 工作范式：规划型、反应式工具调用型、工作流图型
- [ ] 4.3 工具设计：输入、输出、错误、权限、可观测性
- [ ] 4.4 记忆机制：短期状态、长期存储、检索、摘要
- [ ] 4.5 结构化输出与 schema 安全边界
- [ ] 4.6 Agent 评估：trace、回归样例、失败分析

### 模块 5：LangGraph 与工作流 Agent
- [ ] 5.1 LangGraph 心智模型：state、node、edge、条件路由
- [ ] 5.2 构建一个简单的工具调用 graph
- [ ] 5.3 持久化、checkpoint 与 human-in-the-loop
- [ ] 5.4 错误恢复、重试与 graph 级别可观测性
- [ ] 5.5 如何设计可维护的 graph state

### 模块 6：关联 Obsidian 的学习系统
- [ ] 6.1 把 Markdown 当作数据：frontmatter、wikilink、tag、task
- [ ] 6.2 本地文件索引与安全的文件系统工具
- [ ] 6.3 学习记录 schema：session、concept、demo、reflection、review
- [ ] 6.4 对 Obsidian 笔记进行搜索与检索
- [ ] 6.5 让 Agent 创建、更新、链接笔记的工具层
- [ ] 6.6 复习计划与学习进度状态

### 模块 7：最终项目
- [ ] 7.1 API：创建与查询学习 session
- [ ] 7.2 数据库：持久化 concept、demo、note、review
- [ ] 7.3 Agent：根据历史记录和 vault 状态提出下一步学习建议
- [ ] 7.4 Obsidian 集成：生成带 wikilink 和 frontmatter 的 Markdown 记录
- [ ] 7.5 评估：demo 场景与回归测试
- [ ] 7.6 项目收尾：CLI/API 文档、错误状态、部署说明

## 掌握情况快照

<!-- BLOOM:MASTERY_SNAPSHOT:START -->
- [ ] 1.1 HTTP、ASGI 与 FastAPI 请求生命周期
- [ ] 1.2 路由函数、依赖注入与应用结构
- [ ] 1.3 Pydantic schema、数据校验、序列化与响应模型
- [ ] 1.4 错误处理、状态码、中间件与日志
- [ ] 1.5 配置管理、环境变量与应用 settings
- [ ] 2.1 关系型建模：表、主键、外键、约束、索引
- [ ] 2.2 SQLAlchemy 2.0 核心概念：engine、session、model、query
- [x] 2.3 不遮蔽数据库细节的 CRUD 写法
- [x] 2.4 表关系、懒加载/预加载与 N+1 问题
- [ ] 2.5 Alembic 迁移与数据库结构演进
- [ ] 2.6 事务、并发与失败边界
- [ ] 3.1 分层结构：router、service、repository、schema、model
- [ ] 3.2 用依赖注入管理数据库 session 和业务服务
- [ ] 3.3 鉴权基础：用户、密码哈希、JWT/session 取舍
- [ ] 3.4 FastAPI 测试：单元测试、集成测试、测试数据库
- [ ] 3.5 后台任务、队列与长耗时任务
- [ ] 3.6 API 设计：分页、过滤、幂等性、版本管理
- [ ] 4.1 LLM 应用循环：prompt、state、tool call、observation、answer
- [ ] 4.2 三种 Agent 工作范式：规划型、反应式工具调用型、工作流图型
- [ ] 4.3 工具设计：输入、输出、错误、权限、可观测性
- [ ] 4.4 记忆机制：短期状态、长期存储、检索、摘要
- [ ] 4.5 结构化输出与 schema 安全边界
- [ ] 4.6 Agent 评估：trace、回归样例、失败分析
- [ ] 5.1 LangGraph 心智模型：state、node、edge、条件路由
- [ ] 5.2 构建一个简单的工具调用 graph
- [ ] 5.3 持久化、checkpoint 与 human-in-the-loop
- [ ] 5.4 错误恢复、重试与 graph 级别可观测性
- [ ] 5.5 如何设计可维护的 graph state
- [ ] 6.1 把 Markdown 当作数据：frontmatter、wikilink、tag、task
- [ ] 6.2 本地文件索引与安全的文件系统工具
- [ ] 6.3 学习记录 schema：session、concept、demo、reflection、review
- [ ] 6.4 对 Obsidian 笔记进行搜索与检索
- [ ] 6.5 让 Agent 创建、更新、链接笔记的工具层
- [ ] 6.6 复习计划与学习进度状态
- [ ] 7.1 API：创建与查询学习 session
- [ ] 7.2 数据库：持久化 concept、demo、note、review
- [ ] 7.3 Agent：根据历史记录和 vault 状态提出下一步学习建议
- [ ] 7.4 Obsidian 集成：生成带 wikilink 和 frontmatter 的 Markdown 记录
- [ ] 7.5 评估：demo 场景与回归测试
- [ ] 7.6 项目收尾：CLI/API 文档、错误状态、部署说明
<!-- BLOOM:MASTERY_SNAPSHOT:END -->

## 依赖关系

- 1.1 -> 1.2 -> 1.3 -> 1.4 -> 1.5
- 1.3 -> 2.2 -> 2.3
- 2.1 -> 2.2 -> 2.4 -> 2.5 -> 2.6
- 1.2 + 2.3 -> 3.1 -> 3.2 -> 3.4
- 3.1 + 3.2 -> 3.3、3.5、3.6
- 1.3 -> 4.5
- 4.1 -> 4.2 -> 4.3 -> 4.4 -> 4.6
- 4.2 + 4.5 -> 5.1 -> 5.2 -> 5.3 -> 5.4 -> 5.5
- 6.1 -> 6.2 -> 6.3 -> 6.4 -> 6.5 -> 6.6
- 3.x + 5.x + 6.x -> 7.x
