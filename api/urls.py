from django.urls import path
from .controllers import users_router, tweets_router
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router("/users", users_router)
api.add_router("/tweets", tweets_router)

urlpatterns = [
    path("", api.urls),
]
