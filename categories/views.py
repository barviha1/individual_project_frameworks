"""View-функции страниц категорий документов."""
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.documents import filter_documents_by_category
from storage import load_all


# view-функция страницы /categories/: список категорий документов
def categories(request: HttpRequest) -> HttpResponse:
    """Вернуть страницу со списком категорий и числом документов в них."""
    data = load_all()
    items = ""
    for category in data.categories:
        count = len(filter_documents_by_category(data.documents, category))
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <span>
                <strong>{escape(category.name)}</strong><br>
                {escape(category.description)}
            </span>
            <span class="badge bg-primary align-self-center">
                документов: {count}
            </span>
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Категорий пока нет.</li>'
    content = f"""
    <h1>Категории документов</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("HRDocs – категории", content))
