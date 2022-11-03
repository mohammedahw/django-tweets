from ninja import Schema
from datetime import datetime
from uuid import UUID
from . import user
from typing import List, Optional
from . import comments


class TweetOut(Schema):
    id: UUID
    content: str
    created_at: datetime
    likes: int
    user: user.UserOut
    comments: Optional[List[comments.CommentOut]]


class TweetIn(Schema):
    content: str
