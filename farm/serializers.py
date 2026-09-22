"""DRF serializers for farm API requests."""

from rest_framework import serializers


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


class ScriptSerializer(serializers.Serializer):
    script = serializers.CharField(max_length=65536)
    stop_when_done = serializers.BooleanField(required=False, default=True)


class ScriptStatusQuerySerializer(serializers.Serializer):
    run_id = serializers.CharField(max_length=64)
