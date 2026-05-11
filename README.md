# Obsidian Agent Learn

> 用 Obsidian 管理学习过程，用 FastAPI + SQLAlchemy + Agent 工程化地把知识变成可运行的项目。

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-learning-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat-square)
![Obsidian](https://img.shields.io/badge/Obsidian-vault-7C3AED?style=flat-square&logo=obsidian&logoColor=white)

这是一个面向实战的后端与 Agent 学习仓库。它不是单纯的代码合集，而是一套可以持续迭代的学习系统：笔记、练习、demo、复习计划和最终项目路线都放在同一个 Obsidian 友好的目录里。

最终目标是构建一个学习智能体：它可以记录学习 session，关联 Obsidian 笔记，查询历史学习内容，并辅助安排下一步 demo 和复习计划。

## 当前进度

- 已搭建 Obsidian 风格学习 vault
- 已完成 FastAPI 基础笔记与练习入口
- 已完成 SQLAlchemy + SQLite 基础 CRUD demo
- 正在推进 SQLAlchemy relationship loading、懒加载、预加载和 N+1 问题
- 后续将进入分层 FastAPI 应用、Agent tool loop、LangGraph 和 Obsidian 文件工具

## 仓库结构

```text
.
├── fastapi-agent/
│   ├── _meta/                  # 学习状态、知识地图、复习计划
│   ├── notes/                  # 概念笔记
│   ├── exercises/              # 练习题与复盘
│   ├── summaries/              # 阶段总结
│   └── projects/
│       ├── demos.md            # demo 索引
│       ├── roadmap.md          # 项目路线图
│       └── demos/              # 可运行的小项目
│           ├── 01-minimal-fastapi-api/
│           └── 02-sqlalchemy-sqlite-basics/
├── .obsidian/                  # Obsidian vault 配置
├── .vscode/                    # 编辑器配置
└── README.md
```

## 学习路线

| 模块 | 主题 | 目标 |
| --- | --- | --- |
| 1 | 后端开发基本心智模型 | 理解 HTTP、ASGI、FastAPI 请求生命周期、依赖注入和响应模型 |
| 2 | 数据库与 SQLAlchemy | 掌握 engine、session、model、query、CRUD、关系加载和事务边界 |
| 3 | FastAPI 应用架构 | 练习 router、service、repository、schema、model 的分层组织 |
| 4 | Agent 基础 | 理解 prompt、state、tool call、observation、memory 和结构化输出 |
| 5 | LangGraph 工作流 | 用 graph state、node、edge 和 checkpoint 构建可维护 Agent |
| 6 | Obsidian 学习系统 | 把 Markdown、wikilink、frontmatter 和本地文件索引用作知识底座 |
| 7 | 最终项目 | 做出一个 FastAPI + Agent + Obsidian 的学习助手 |

完整知识地图见 [fastapi-agent/_meta/knowledge-map.md](fastapi-agent/_meta/knowledge-map.md)。

## 快速开始

克隆仓库：

```bash
git clone git@github.com:www0527-ux/obsidian-agent-learn.git
cd obsidian-agent-learn
conda env create -f environment.yml
conda activate obsidian-agent-learn
```

用 Obsidian 打开当前目录，就可以把 `fastapi-agent` 当作学习 vault 阅读和维护。

运行第一个 FastAPI demo：

```bash
cd fastapi-agent/projects/demos/01-minimal-fastapi-api
conda env create -f environment.yml
conda activate fastapi-demo-01
uvicorn app.main:app --reload
```

运行 SQLAlchemy + SQLite demo：

```bash
cd fastapi-agent/projects/demos/02-sqlalchemy-sqlite-basics
conda env create -f environment.yml
conda activate sqlalchemy-sqlite-demo
python main.py
python practice.py
```

## Demo 亮点

### 01 Minimal FastAPI API

一个最小可运行 FastAPI API，用来观察：

- 路由函数如何接收请求
- Pydantic 如何完成数据校验
- FastAPI 如何生成响应和 OpenAPI 文档

### 02 SQLAlchemy + SQLite Basics

一个拆分成 `db.py`、`models.py`、`crud.py`、`loading_examples.py`、`practice.py` 的 SQLAlchemy 2.0 demo，用来观察：

- `engine -> model -> session -> select` 的核心流
- `session.add()`、`commit()`、`refresh()` 的持久化过程
- 懒加载、`selectinload()`、`joinedload()` 的 SQL 差异
- relationship loading 和 N+1 问题

## 工作方式

这个仓库推荐按“小步学习 + 小步验证 + 小步记录”的方式推进：

1. 先看 `_meta/current.md`，确认当前位置、复习项和下一步文件；工具需要结构化状态时读 `_meta/state-lite.json`。
2. 再看 `_meta/knowledge-map.md`，确认今天要学的 1-2 个概念。
3. 阅读 `notes/` 中的概念笔记。
4. 完成 `exercises/` 里的练习。
5. 在 `projects/demos/` 写一个小 demo，把概念跑起来。
6. 用自己的话在 `summaries/` 写短总结。
7. 更新 `_meta/current.md`、`_meta/state-lite.json`、`_meta/progress.md` 和 `_meta/spaced-repetition.md`，保留学习轨迹。

## 最终作品方向

最终项目会是一个学习 Agent 后端，计划包含：

- 学习 session 的创建与查询 API
- concept、demo、note、review 的数据库持久化
- 根据历史记录推荐下一步学习内容
- 自动生成带 frontmatter 和 wikilink 的 Obsidian Markdown
- 基于 demo 场景的回归测试与评估

## 备注

这个仓库会随着学习推进持续变化。每个 demo 都会尽量保持小而完整，优先解释一个清晰问题，而不是一次性堆满所有功能。
