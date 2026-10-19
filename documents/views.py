"""View-функции страниц документов."""
from datetime import date
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.documents import (
    Document,
    find_document_by_id,
    get_documents_statistics,
    sort_documents_by_expiry,
)
from storage import load_all


# подготовка строк для шаблона: документ, его статус и дата окончания
def build_document_rows(
    documents: list[Document], today: date
) -> list[dict[str, Any]]:
    """Вернуть данные документов для шаблона.

    Статус вычисляется методом get_status() в Python: он принимает
    аргумент (дату), а шаблон Django методы с аргументами не вызывает.
    """
    return [
        {
            "document": document,
            "status": document.get_status(today),
            "expiry": date.fromisoformat(document.expiry_date),
        }
        for document in documents
    ]


# view-функция страницы /documents/: список документов и статистика сроков
def documents(request: HttpRequest) -> HttpResponse:
    """Вернуть страницу со списком документов из data/documents.json."""
    today = date.today()
    documents_list = load_all().documents

    context = {
        "stats": get_documents_statistics(documents_list, today),
        "document_rows": build_document_rows(
            sort_documents_by_expiry(documents_list), today
        ),
    }
    return render(request, "documents/document_list.html", context)


# view-функция страницы /documents/<id>/: карточка документа
def document_detail(request: HttpRequest, document_id: int) -> HttpResponse:
    """Вернуть страницу документа или ответ с кодом 404."""
    documents_list = load_all().documents
    document = find_document_by_id(documents_list, document_id)

    context: dict[str, Any] = {"document": document}
    if document is not None:
        today = date.today()
        context["status"] = document.get_status(today)
        context["expiry"] = date.fromisoformat(document.expiry_date)

    return render(
        request,
        "documents/document_detail.html",
        context,
        status=404 if document is None else 200,
    )
