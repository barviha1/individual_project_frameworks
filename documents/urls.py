"""Маршруты приложения documents."""
from django.urls import path

from . import views

app_name = "documents"

urlpatterns = [
    path("", views.documents, name="list"),
    path("<int:document_id>/", views.document_detail, name="detail"),
]
