"""DeviceFarm provider client implementation."""

from __future__ import annotations

from typing import Any

import requests

from .base import PhoneFarmProviderClient
from .exceptions import ProviderAPIError


class DeviceFarmClient(PhoneFarmProviderClient):
    """Client for https://devicefarm.io/api/v1 endpoints."""

    def __init__(self, api_key: str, base_url: str = "https://devicefarm.io/api/v1"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        try:
            response = self.session.request(
                method=method,
                url=f"{self.base_url}{path}",
                params=params,
                json=json,
                timeout=30,
            )
        except requests.RequestException as exc:
            raise ProviderAPIError(str(exc)) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise ProviderAPIError("Provider returned non-JSON response", status_code=response.status_code) from exc

        provider_error = payload.get("error")
        if provider_error:
            raise ProviderAPIError(
                message=provider_error.get("message", "Provider API error"),
                code=provider_error.get("code"),
                status_code=response.status_code,
            )

        if payload.get("data") is None:
            raise ProviderAPIError("Provider API returned empty data envelope", status_code=response.status_code)

        return payload["data"]

    def list_phones(self, *, limit: int | None = None) -> list[dict[str, Any]]:
        params = {"limit": limit} if limit is not None else None
        return self._request("GET", "/phones", params=params)

    def create_phone(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/phones", json=payload)

    def start_phone(self, phone_id: str) -> dict[str, Any]:
        return self._request("POST", f"/phones/{phone_id}/start")

    def stop_phone(self, phone_id: str) -> dict[str, Any]:
        return self._request("POST", f"/phones/{phone_id}/stop")

    def prepare_phone(self, phone_id: str, *, packages: list[str] | None = None) -> dict[str, Any]:
        payload = {"packages": packages or []}
        return self._request("POST", f"/phones/{phone_id}/prepare", json=payload)

    def run_shell(self, phone_id: str, *, cmd: str) -> dict[str, Any]:
        return self._request("POST", f"/phones/{phone_id}/shell", json={"cmd": cmd})

    def run_script(self, phone_id: str, *, script: str, stop_when_done: bool = True) -> dict[str, Any]:
        payload = {"script": script, "stop_when_done": stop_when_done}
        return self._request("POST", f"/phones/{phone_id}/script", json=payload)

    def script_status(self, phone_id: str, *, run_id: str) -> dict[str, Any]:
        return self._request("GET", f"/phones/{phone_id}/script", params={"run_id": run_id})

    def delete_phone(self, phone_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"/phones/{phone_id}")
