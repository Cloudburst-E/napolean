"""API views for mobile phone farm provider integrations."""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .providers.exceptions import ProviderAPIError
from .providers.registry import get_provider_client
from .serializers import (
    CreatePhoneSerializer,
    ListPhonesQuerySerializer,
    PreparePhoneSerializer,
    ScriptSerializer,
    ScriptStatusQuerySerializer,
    ShellSerializer,
)


class ProviderIndexView(APIView):
    def get(self, request):
        return Response({"providers": ["devicefarm"]})


class ProviderPhonesView(APIView):
    def get(self, request, provider_name: str):
        try:
            provider_client = get_provider_client(provider_name)
            serializer = ListPhonesQuerySerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            phones = provider_client.list_phones(limit=serializer.validated_data.get("limit"))
        except ProviderAPIError as exc:
            return _provider_error_response(exc)
        return Response({"data": phones})

    def post(self, request, provider_name: str):
        try:
            provider_client = get_provider_client(provider_name)
            serializer = CreatePhoneSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone = provider_client.create_phone(serializer.validated_data)
        except ProviderAPIError as exc:
            return _provider_error_response(exc)
        return Response({"data": phone}, status=status.HTTP_201_CREATED)


class PhoneActionView(APIView):
    def post(self, request, provider_name: str, phone_id: str, action: str):
        try:
            provider_client = get_provider_client(provider_name)
            if action == "start":
                result = provider_client.start_phone(phone_id)
            elif action == "stop":
                result = provider_client.stop_phone(phone_id)
            elif action == "prepare":
                serializer = PreparePhoneSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                result = provider_client.prepare_phone(phone_id, packages=serializer.validated_data.get("packages"))
            elif action == "shell":
                serializer = ShellSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                result = provider_client.run_shell(phone_id, cmd=serializer.validated_data["cmd"])
            else:
                raise ProviderAPIError(
                    f"Unsupported action '{action}'",
                    code="unsupported_action",
                    status_code=404,
                )
        except ProviderAPIError as exc:
            return _provider_error_response(exc)
        return Response({"data": result})


class ScriptView(APIView):
    def post(self, request, provider_name: str, phone_id: str):
        try:
            provider_client = get_provider_client(provider_name)
            serializer = ScriptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = provider_client.run_script(
                phone_id,
                script=serializer.validated_data["script"],
                stop_when_done=serializer.validated_data.get("stop_when_done", True),
            )
        except ProviderAPIError as exc:
            return _provider_error_response(exc)
        return Response({"data": result})

    def get(self, request, provider_name: str, phone_id: str):
        try:
            provider_client = get_provider_client(provider_name)
            serializer = ScriptStatusQuerySerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            result = provider_client.script_status(phone_id, run_id=serializer.validated_data["run_id"])
        except ProviderAPIError as exc:
            return _provider_error_response(exc)
        return Response({"data": result})


class DeletePhoneView(APIView):
    def delete(self, request, provider_name: str, phone_id: str):
        try:
            provider_client = get_provider_client(provider_name)
            result = provider_client.delete_phone(phone_id)
        except ProviderAPIError as exc:
            return _provider_error_response(exc)
        return Response({"data": result})


def _provider_error_response(error: ProviderAPIError) -> Response:
    status_code = error.status_code or status.HTTP_502_BAD_GATEWAY
    if error.code == "unsupported_provider":
        message = "Unsupported provider."
    elif error.code == "provider_not_configured":
        message = "Provider is not configured."
    elif status_code >= 500:
        message = "Provider request failed."
    else:
        message = "Provider request rejected."

    return Response(
        {
            "data": None,
            "error": {
                "code": error.code or "provider_error",
                "message": message,
            },
        },
        status=status_code,
    )
