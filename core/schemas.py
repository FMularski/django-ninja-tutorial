from datetime import datetime

from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema

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
