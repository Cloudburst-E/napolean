"""Abstract provider API clients for mobile phone farms."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PhoneFarmProviderClient(ABC):
    """Contract for hardware-as-a-service provider integrations."""

    @abstractmethod
    def list_phones(self, *, limit: int | None = None) -> list[dict[str, Any]]:
        """List phones available on the provider account."""

    @abstractmethod
    def create_phone(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a new phone."""

    @abstractmethod
    def start_phone(self, phone_id: str) -> dict[str, Any]:
        """Start an existing phone."""

    @abstractmethod
    def stop_phone(self, phone_id: str) -> dict[str, Any]:
        """Stop a running phone."""

    @abstractmethod
    def prepare_phone(self, phone_id: str, *, packages: list[str] | None = None) -> dict[str, Any]:
        """Install provider automation library on a running phone."""

    @abstractmethod
    def run_shell(self, phone_id: str, *, cmd: str) -> dict[str, Any]:
        """Run a single command."""

    @abstractmethod
    def run_script(self, phone_id: str, *, script: str, stop_when_done: bool = True) -> dict[str, Any]:
        """Run a detached script."""

    @abstractmethod
    def script_status(self, phone_id: str, *, run_id: str) -> dict[str, Any]:
        """Poll detached script status."""

    @abstractmethod
    def delete_phone(self, phone_id: str) -> dict[str, Any]:
        """Delete a phone permanently."""
