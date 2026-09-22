"""Exceptions raised by provider clients."""


class ProviderAPIError(Exception):
    """Represents a provider API failure with optional metadata."""

    def __init__(self, message: str, code: str | None = None, status_code: int | None = None):
        super().__init__(message)
        self.code = code
        self.status_code = status_code
