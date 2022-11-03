from ninja import Router
from api import models
from django.conf import settings
from api.schemas import auth
import jwt
from ninja.errors import HttpError
from django.contrib.auth.hashers import make_password, check_password

router = Router(tags=['auth'])


@router.post("/login", response=auth.AuthOut)
def login(request, payload: auth.LoginIn):
    user = models.User.objects.get(username=payload.username)
    is_valid = check_password(payload.password, user.password)

    if not is_valid:
        raise HttpError(400, "invalid credentials")

    token_payload = {"id": str(user.id)}
    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm="HS256")
    response = {"user": user, "token": token}
    return response


@router.post("/register", response=auth.AuthOut)
def register(request, payload: auth.RegisterIn):
    payload.password = make_password(password=payload.password)
    user = models.User.objects.create(**payload.dict())
    token_payload = {"id": str(user.id)}
    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm="HS256")
    response = {"user": user, "token": token}

    return response
