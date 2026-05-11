# Demo 02: SQLAlchemy + SQLite Basics

## Goal

This demo is for learning SQLAlchemy 2.0's core flow:

```text
engine -> model -> session -> select
```

It uses SQLite, so no separate database server is required. Running the script creates a local `demo.db` file in this folder.

## Run

From this directory:

```bash
python main.py
```

Expected output:

```text
Inserted user: id=1, username=alice
Queried user: id=1, username=alice, email=alice@example.com
All users:
- 1 alice alice@example.com
```

## What To Observe

- `engine` knows how to connect to the database.
- `Base.metadata.create_all(engine)` creates tables from model definitions.
- `User` maps a Python class to the `users` table.
- `Session(engine)` opens a database work unit.
- `session.add(user)` stages a new row.
- `session.commit()` persists the row.
- `session.refresh(user)` reloads generated fields such as `id`.
- `select(User)` builds a query.
- `session.scalar(...)` executes a query and returns one ORM object.

## Relationship Loading Practice

The later practice files split the demo into smaller modules:

```text
db.py
models.py
crud.py
loading_examples.py
practice.py
```

Run:

```bash
python practice.py
```

Observe the SQL emitted by:

- `list_users_lazy()`
- `list_users_with_selectinload()`
- `list_users_with_joinedload()`
