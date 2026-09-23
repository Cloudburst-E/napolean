"""Provider client registry."""

import os

from .base import PhoneFarmProviderClient
from .devicefarm import DeviceFarmClient
from .exceptions import ProviderAPIError


def get_provider_client(provider_name: str) -> PhoneFarmProviderClient:
    normalized_name = provider_name.lower().strip()
    if normalized_name == "devicefarm":
        api_key = os.environ.get("DEVICEFARM_API_KEY", "").strip()
        if not api_key:
            raise ProviderAPIError(
                "Missing DEVICEFARM_API_KEY environment variable",
                code="provider_not_configured",
                status_code=500,
            )
        return DeviceFarmClient(api_key=api_key)
    raise ProviderAPIError(
        f"Unsupported provider '{provider_name}'",
        code="unsupported_provider",
        status_code=404,
    )
