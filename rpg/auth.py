from typing import Any

from django.http import HttpRequest
from ninja.security import APIKeyHeader


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request: HttpRequest, key: str | None) -> Any | None:
        if key == "classified":
            return key
