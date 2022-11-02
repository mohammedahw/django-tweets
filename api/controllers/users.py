from ninja import Router
from api import models
from django.conf import settings
from api.schemas import user, tweets
from typing import List
from uuid import UUID
from ninja.pagination import paginate, LimitOffsetPagination
from api.auth import BearerAuth
from ninja.errors import HttpError

router = Router(tags=['users'])


@router.get("", response=List[user.UserOut])
@paginate(LimitOffsetPagination)
def find_all(request):
    users = models.User.objects.all()
    return users


@router.get("/{user_id}", response=user.UserOut)
def find_one(request, user_id: UUID):
    user = models.User.objects.get(id=user_id)
    return user


@router.delete("/{user_id}", response=user.UserOut, auth=BearerAuth())
def delete(request, user_id: UUID):
    user = models.User.objects.get(id=user_id)
    if not user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")
    user.delete()
    return user
