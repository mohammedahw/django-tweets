from ninja import Schema
from datetime import datetime
from uuid import UUID


class TweetOut(Schema):
    id: UUID
    content: str
    created_at: datetime
    likes: int
    user_id: str


class TweetIn(Schema):
    content: str
    user_id: UUID
