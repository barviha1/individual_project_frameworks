"""Главная страница и общий HTML-каркас всех страниц проекта."""
from django.http import HttpRequest, HttpResponse


# функция формирования единого HTML-каркаса страницы (Bootstrap + навигация)
def page(title: str, content: str) -> str:
    """Собрать HTML-документ: кодировка, заголовок, Bootstrap, навигация."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/employees/">Сотрудники</a>
        <a class="nav-link" href="/documents/">Документы</a>
        <a class="nav-link" href="/categories/">Категории</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


# функция формирования цветного бейджа статуса срока действия документа
def status_badge(status: str) -> str:
    """Вернуть HTML-бейдж, цвет которого зависит от статуса документа."""
    colors = {
        "Активен": "bg-success",
        "Скоро истекает": "bg-warning text-dark",
        "Истёк": "bg-danger",
    }
    color = colors.get(status, "bg-secondary")
    return f'<span class="badge {color}">{status}</span>'


# view-функция главной страницы: описание приложения и навигация
def index(request: HttpRequest) -> HttpResponse:
    """Вернуть главную страницу проекта."""
    content = """
    <h1 class="display-4">HRDocs</h1>
    <p class="lead">Система управления кадровыми документами.</p>
    <p>Основные разделы:</p>
    <a href="/employees/" class="btn btn-primary me-2">Сотрудники</a>
    <a href="/documents/" class="btn btn-secondary me-2">Документы</a>
    <a href="/categories/" class="btn btn-secondary">Категории</a>
    """
    return HttpResponse(page("HRDocs", content))


# обработчик handler404: страница ошибки 404 в оформлении проекта
def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Вернуть собственную страницу 404 с кодом статуса 404."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
