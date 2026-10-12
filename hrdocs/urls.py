"""Корневая маршрутизация проекта: распределение адресов по приложениям."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("employees/", include("employees.urls")),
    path("categories/", include("categories.urls")),
    path("documents/", include("documents.urls")),
]

# обработчик ошибки 404: собственная страница проекта (при DEBUG = False)
handler404 = "homepage.views.page_not_found"
