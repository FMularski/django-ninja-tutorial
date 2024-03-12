from http import HTTPStatus

from django.contrib.auth import authenticate
from knox.models import AuthToken
from ninja import NinjaAPI

from core.schemas import LoginCredentialsSchema, TokenResponseSchema, UnauthorizedResponseSchema

api = NinjaAPI(urls_namespace="core")


@api.post(
    "login/",
    response={
        HTTPStatus.OK: TokenResponseSchema,
        HTTPStatus.UNAUTHORIZED: UnauthorizedResponseSchema,
    },
)
def login(request, credentials: LoginCredentialsSchema):
    user = authenticate(request, username=credentials.username, password=credentials.password)
    if user:
        _, token = AuthToken.objects.create(user)
        return HTTPStatus.OK, {"token": token}

    return HTTPStatus.UNAUTHORIZED, "Authentication failed."
