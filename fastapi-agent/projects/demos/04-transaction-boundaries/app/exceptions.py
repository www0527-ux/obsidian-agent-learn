from __future__ import annotations


class UserNameConflictError(Exception):
    """Raised when the database rejects a duplicate user name."""
    def __init__(self, name: str) -> None:
        super().__init__(f"User name '{name}' already exists.")

class record_increment_conflict_error(Exception):
    """Raised when the database rejects a concurrent update to the same record."""
    def __init__(self, record_id: int) -> None:
        super().__init__(f"Record with id '{record_id}' has been concurrently updated.")