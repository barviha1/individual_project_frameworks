"""Маршруты приложения categories."""
from django.urls import path

from . import views

app_name = "categories"

urlpatterns = [
    path("", views.categories, name="list"),
]
