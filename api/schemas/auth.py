from ninja import Schema
from uuid import UUID
from .user import UserOut


class AuthOut(Schema):
    user: UserOut
    token: str


class RegisterIn(Schema):
    username: str
    bio: str
    password: str


class LoginIn(Schema):
    username: str
    password: str
