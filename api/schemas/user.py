from ninja import Schema

from uuid import UUID

from datetime import datetime


class UserOut(Schema):
    id: UUID
    username: str
    bio: str
    created_at: datetime
