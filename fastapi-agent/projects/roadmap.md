# 项目路线图

## Demo 练习线

这些 demo 是独立小项目，用来分别打牢知识点。每个 demo 都不追求大而全，而是专门解决一个能力缺口。

1. `demos/01-minimal-fastapi-api`：HTTP、ASGI、路由函数、请求体验证。
2. `demos/02-crud-sqlalchemy-sqlite`：SQLAlchemy 2.0、CRUD、事务。
3. `demos/03-fastapi-layered-crud`：router/service/repository 分层。
4. `demos/04-auth-and-tests`：鉴权基础和测试数据库。
5. `demos/05-agent-tool-loop`：最小工具调用 Agent。
6. `demos/06-langgraph-study-planner`：用 LangGraph 做学习计划工作流。
7. `demos/07-obsidian-file-tools`：安全读取、创建、链接 Markdown 笔记。

## 最终项目

`final-learning-agent` 是最终应用：一个 FastAPI 后端 + Agent 工作流。它可以管理学习 session、概念、demo、复习计划，并把记录写入 Obsidian。

### 里程碑

- M1：用 SQLite 做学习记录 API。
- M2：完成 concept 和 demo 的 CRUD，并补上测试。
- M3：实现 Obsidian Markdown 写入器，支持 wikilink 和 frontmatter。
- M4：为 Agent 设计读写学习记录的工具层。
- M5：用 LangGraph 做一个能提出下一步学习建议的 planner。
- M6：补齐评估场景、回归测试和最终文档。

