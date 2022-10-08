from ninja import Schema

from uuid import UUID

from datetime import datetime


class UserOut(Schema):

    id: UUID
    username: str

    bio: str

    created_at: datetime


class LoginAndRegisterOut(Schema):

    user: UserOut

    token: str


class UserRegisterIn(Schema):
    username: str

    bio: str

    password: str


class UserLoginIn(Schema):
    username: str

    password: str
