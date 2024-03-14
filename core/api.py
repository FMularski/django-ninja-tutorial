from http import HTTPStatus

from django.contrib.auth import authenticate
from knox.models import AuthToken
from ninja import Router

from core.schemas import LoginCredentialsSchema, TokenResponseSchema, UnauthorizedResponseSchema

router = Router(tags=["Core"])


@router.post(
    "login/",
    response={
        HTTPStatus.OK: TokenResponseSchema,
        HTTPStatus.UNAUTHORIZED: UnauthorizedResponseSchema,
    },
    auth=None,  # exclude this endpoint from global authorization
)
def login(request, credentials: LoginCredentialsSchema):
    user = authenticate(request, username=credentials.username, password=credentials.password)
    if user:
        token_instance, token = AuthToken.objects.create(user)

        return HTTPStatus.OK, {
            "user": token_instance.user,
            "token": token,
            "expiry": token_instance.expiry,
        }

    return HTTPStatus.UNAUTHORIZED, {"message": "Authentication failed."}
