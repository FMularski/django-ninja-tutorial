from datetime import datetime
from http import HTTPStatus
from typing import ClassVar

from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.db.models import QuerySet
from ninja import ModelSchema, Schema
from ninja.errors import HttpError

User = get_user_model()


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )


class LoginCredentialsSchema(Schema):
    username: str
    password: str


class TokenResponseSchema(Schema):
    user: UserSchema
    token: str
    expiry: datetime


class UnauthorizedResponseSchema(Schema):
    message: str


class OrderSchema(Schema):
    ordering: str | None = None

    # mark these fields as class variables
    # which are not supposed to be query params
    separator: ClassVar[str] = ","
    raise_bad_request: ClassVar[bool] = True

    def order(self, queryset: QuerySet) -> QuerySet:
        if not self.ordering:
            return queryset

        ordering_fields = self.ordering.split(self.separator)

        try:
            ordered = queryset.order_by(*ordering_fields)
        except FieldError as e:
            if self.raise_bad_request:
                raise HttpError(HTTPStatus.BAD_REQUEST, str(e))

            return queryset

        return ordered
