from ninja import Schema


class LoginCredentialsSchema(Schema):
    username: str
    password: str


class TokenResponseSchema(Schema):
    token: str


class UnauthorizedResponseSchema(Schema):
    message: str
