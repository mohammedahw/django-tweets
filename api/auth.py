import jwt
from ninja.security import HttpBearer
from django.conf import settings


class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            return {"id": payload.get("id")}
        except jwt.PyJWTError:
            return {"error": "invalid token"}
