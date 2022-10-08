from ninja import Schema
from uuid import UUID
from . import user
from datetime import datetime


class CommentIn(Schema):
    content: str


class CommentOut(Schema):
    id: UUID
    content: str
    tweet_id: UUID
    user: user.UserOut
    created_at: datetime
