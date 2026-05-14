from __future__ import annotations

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# 1. 导入项目里的 ORM 基类和模型模块
#
# Base 是所有 ORM 模型共同继承的基类，Base.metadata 里会收集所有表结构。
# Alembic 的 autogenerate 会拿 target_metadata 和真实数据库结构做对比。
from app.db import Base

# 这行看起来“没有被使用”，但它很重要：
# 导入 app.models 会让 User、LearningRecord 等模型类被 Python 执行并注册到
# Base.metadata 中。否则 Base.metadata 可能是空的，Alembic 就不知道有哪些表。
from app import models  # noqa: F401


# 2. 读取 Alembic 的配置对象
#
# context.config 来自 alembic.ini。里面包含 script_location、sqlalchemy.url、
# 日志配置等信息。env.py 运行时，Alembic 会把这个 config 注入进来。
config = context.config

# 3. 配置日志
#
# 如果 alembic.ini 存在，就按其中的 [loggers]、[handlers]、[formatters]
# 初始化日志。这样执行 alembic 命令时能看到 INFO/WARNING 等输出。
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# 4. 连接 Alembic 和 SQLAlchemy ORM
#
# 这是 env.py 最关键的一行。
# target_metadata 告诉 Alembic：“当前代码希望数据库最终长这样。”
# 使用 autogenerate 时，Alembic 会比较：
# - 数据库当前真实结构
# - Base.metadata 中记录的 ORM 模型结构
# 然后生成迁移脚本草稿。
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """在 offline 模式下生成迁移 SQL，不直接连接数据库。"""

    # 从 alembic.ini 读取 sqlalchemy.url。
    # offline 模式只需要数据库 URL，用它判断方言，例如 sqlite/postgresql。
    url = config.get_main_option("sqlalchemy.url")

    # 配置 Alembic 迁移上下文。
    #
    # url:
    #   只提供数据库地址，不创建真实 connection。
    # target_metadata:
    #   提供 ORM 表结构，用于 autogenerate 对比。
    # literal_binds=True:
    #   生成 SQL 文本时，尽量把参数值直接写进 SQL。
    # dialect_opts:
    #   告诉 SQLAlchemy 使用 named 风格的参数名。
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # 迁移操作要包在事务里。
    # context.run_migrations() 会按 versions/ 里的迁移脚本执行 upgrade/downgrade。
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在 online 模式下连接数据库并执行迁移。"""

    # 从 alembic.ini 的当前配置段读取 sqlalchemy.* 配置，
    # 例如 sqlalchemy.url = sqlite:///alembic_template.db。
    #
    # prefix="sqlalchemy." 表示只取 sqlalchemy. 开头的配置项。
    # pool.NullPool 表示不使用连接池；迁移命令通常是短生命周期任务，
    # 不需要像 Web 服务那样长期维护数据库连接池。
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # 创建真实数据库连接。
    with connectable.connect() as connection:
        # 把 connection 交给 Alembic，并提供 target_metadata。
        # 之后 Alembic 就可以在这个连接上执行迁移 SQL。
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        # 和 offline 一样，真实执行迁移也要包在事务中。
        with context.begin_transaction():
            context.run_migrations()


# 5. 根据 Alembic 当前运行模式选择执行路径
#
# 常见情况：
# - alembic upgrade head     -> online，真实连接数据库并执行迁移
# - alembic upgrade head --sql -> offline，只输出 SQL，不执行
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
