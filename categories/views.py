"""View-функции страниц категорий документов."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.documents import filter_documents_by_category
from storage import load_all


# view-функция страницы /categories/: список категорий документов
def categories(request: HttpRequest) -> HttpResponse:
    """Вернуть страницу со списком категорий и числом документов в них."""
    data = load_all()
    context = {
        "category_rows": [
            {
                "category": category,
                "count": len(
                    filter_documents_by_category(data.documents, category)
                ),
            }
            for category in data.categories
        ],
    }
    return render(request, "categories/category_list.html", context)
