"""Главная страница и обработчик ошибки 404."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# view-функция главной страницы: данных нет, контекст не нужен
def index(request: HttpRequest) -> HttpResponse:
    """Вернуть главную страницу проекта."""
    return render(request, "homepage/index.html")


# обработчик handler404: страница ошибки 404 в оформлении проекта
def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Вернуть собственную страницу 404 с кодом статуса 404."""
    return render(request, "homepage/404.html", status=404)
