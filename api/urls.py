from django.urls import path
from .controller import controller

urlpatterns = [
    path("", controller.urls)
]
