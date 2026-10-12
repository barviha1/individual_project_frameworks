"""Маршруты приложения documents."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.documents, name="documents"),
    path("<int:document_id>/", views.document_detail, name="document_detail"),
]
