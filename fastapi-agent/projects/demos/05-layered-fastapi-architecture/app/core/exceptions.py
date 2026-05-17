from __future__ import annotations


class AppError(Exception):
    """Base class for business-level errors."""


class UserNotFoundError(AppError):
    # TODO: store user_id and provide a useful message.
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with id {user_id} not found.")


class UserNameConflictError(AppError):
    # TODO: store name and provide a useful message.
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"User with name {name} already exists.")
