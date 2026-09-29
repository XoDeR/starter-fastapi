class AppError(Exception):
    """Base class for domain errors raised below the web layer."""


class InvalidCredentialsError(AppError):
    """Email and password did not match an account."""


class EmailAlreadyRegisteredError(AppError):
    """An account with this email already exists."""


class BookNotFoundError(AppError):
    """The book does not exist for the current user."""
