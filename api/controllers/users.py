from ninja import Router
from api import models

from django.conf import settings


from api.schemas import user, tweets

from typing import List

from uuid import UUID

from ninja.pagination import paginate, LimitOffsetPagination

from api.auth import BearerAuth

import jwt

from ninja.errors import HttpError

from django.contrib.auth.hashers import make_password, check_password

router = Router(tags=['users'])


@router.post("/login", response=user.LoginAndRegisterOut)
def login(request, payload: user.UserLoginIn):

    user = models.User.objects.get(

        username=payload.username)

    is_valid = check_password(payload.password, user.password)

    if not is_valid:

        raise HttpError(400, "invalid credentials")

    token_payload = {"id": str(user.id)}

    token = jwt.encode(token_payload, settings.SECRET_KEY,

                       algorithm="HS256")

    response = {"user": user, "token": token}

    return response


@router.get("", response=List[user.UserOut])
@paginate(LimitOffsetPagination)
def find_all(request):

    users = models.User.objects.all()
    return users


@router.get("/{user_id}", response=user.UserOut)
def find_one(request, user_id: UUID):

    user = models.User.objects.get(id=user_id)
    return user


@router.post("", response=user.LoginAndRegisterOut)
def register(request, payload: user.UserRegisterIn):

    payload.password = make_password(password=payload.password)

    user = models.User.objects.create(**payload.dict())

    token_payload = {"id": str(user.id)}

    token = jwt.encode(token_payload, settings.SECRET_KEY,

                       algorithm="HS256")

    response = {"user": user, "token": token}
    return response


@router.delete("/{user_id}", response=user.UserOut, auth=BearerAuth())
def delete(request, user_id: UUID):

    user = models.User.objects.get(id=user_id)
    if not user.id == request.auth['id']:
        raise HttpError(401, "Unauthorized")
    user.delete()
    return user
