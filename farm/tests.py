from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase


class _StubProviderClient:
    def list_phones(self, *, limit=None):
        return [{"id": "abc", "status": "stopped", "limit": limit}]

    def create_phone(self, payload):
        return {"id": "created", **payload}

    def start_phone(self, phone_id):
        return {"id": phone_id, "status": "starting"}

    def stop_phone(self, phone_id):
        return {"id": phone_id, "status": "stopped"}

    def prepare_phone(self, phone_id, *, packages=None):
        return {"id": phone_id, "packages": packages or []}

    def run_shell(self, phone_id, *, cmd):
        return {"id": phone_id, "cmd": cmd}

    def run_script(self, phone_id, *, script, stop_when_done=True):
        return {"id": phone_id, "script": script, "stop_when_done": stop_when_done}

    def script_status(self, phone_id, *, run_id):
        return {"id": phone_id, "run_id": run_id, "running": False}

    def delete_phone(self, phone_id):
        return {"id": phone_id, "deleted": True}


class FarmApiTests(APITestCase):
    def test_provider_index(self):
        response = self.client.get("/api/providers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"providers": ["devicefarm"]})

    @patch("farm.views.get_provider_client", return_value=_StubProviderClient())
    def test_list_phones(self, _):
        response = self.client.get("/api/providers/devicefarm/phones", {"limit": 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"][0]["limit"], 3)

    @patch("farm.views.get_provider_client", return_value=_StubProviderClient())
    def test_create_phone(self, _):
        payload = {
            "name": "US warmup 01",
            "deviceBrand": "Samsung",
            "deviceModel": "Galaxy A55",
            "proxy": {"mode": "saved", "proxyId": "123"},
        }
        response = self.client.post("/api/providers/devicefarm/phones", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["data"]["id"], "created")

    @patch("farm.views.get_provider_client", return_value=_StubProviderClient())
    def test_script_status(self, _):
        response = self.client.get("/api/providers/devicefarm/phones/abc/script", {"run_id": "run_1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["run_id"], "run_1")
