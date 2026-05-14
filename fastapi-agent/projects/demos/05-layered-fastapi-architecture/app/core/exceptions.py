from __future__ import annotations


class AppError(Exception):
    """Base class for business-level errors."""


class UserNotFoundError(AppError):
    # TODO: store user_id and provide a useful message.
    pass


class UserNameConflictError(AppError):
    # TODO: store name and provide a useful message.
    pass
