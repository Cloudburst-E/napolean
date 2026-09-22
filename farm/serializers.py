"""DRF serializers for farm API requests."""

import re

from rest_framework import serializers


FORBIDDEN_INPUT_COMMAND_PATTERN = re.compile(r"\binput\s+(tap|swipe|touchscreen)\b", flags=re.IGNORECASE)
HUMANIZE_SOURCE_PATTERN = re.compile(r"(^|\n)\s*(\.|source)\s+/data/local/tmp/humanize\.sh(\s|$)")


class ListPhonesQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(required=False, min_value=1, max_value=200)


class CreatePhoneSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    deviceBrand = serializers.CharField(max_length=100)
    deviceModel = serializers.CharField(max_length=100)
    androidVersion = serializers.CharField(required=False, max_length=50)
    proxy = serializers.JSONField()
    datacenter = serializers.CharField(required=False, max_length=20)
    region = serializers.CharField(required=False, max_length=100)
    language = serializers.CharField(required=False, max_length=100)
    netType = serializers.CharField(required=False, max_length=20)
    tags = serializers.ListField(required=False, child=serializers.CharField(max_length=100), max_length=20)
    group = serializers.CharField(required=False, max_length=255)
    note = serializers.CharField(required=False, max_length=1500)


class PreparePhoneSerializer(serializers.Serializer):
    packages = serializers.ListField(required=False, child=serializers.CharField(max_length=255), max_length=20)


class ShellSerializer(serializers.Serializer):
    cmd = serializers.CharField(max_length=8192)

    def validate_cmd(self, value: str) -> str:
        if FORBIDDEN_INPUT_COMMAND_PATTERN.search(value):
            raise serializers.ValidationError(
                "Use h_* helpers from /data/local/tmp/humanize.sh instead of input tap/swipe/touchscreen."
            )
        return value


class ScriptSerializer(serializers.Serializer):
    script = serializers.CharField(max_length=65536)
    stop_when_done = serializers.BooleanField(required=False, default=True)

    def validate_script(self, value: str) -> str:
        if FORBIDDEN_INPUT_COMMAND_PATTERN.search(value):
            raise serializers.ValidationError(
                "Use h_* helpers from /data/local/tmp/humanize.sh instead of input tap/swipe/touchscreen."
            )
        if not HUMANIZE_SOURCE_PATTERN.search(value):
            raise serializers.ValidationError(
                "Scripts must source /data/local/tmp/humanize.sh once per run."
            )
        return value


class ScriptStatusQuerySerializer(serializers.Serializer):
    run_id = serializers.CharField(max_length=64)
