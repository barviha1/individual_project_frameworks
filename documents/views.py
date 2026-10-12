"""View-функции страниц документов."""
from datetime import date

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page, status_badge
from models.documents import (
    find_document_by_id,
    get_documents_statistics,
    sort_documents_by_expiry,
)
from storage import load_all


# view-функция страницы /documents/: список документов и статистика сроков
def documents(request: HttpRequest) -> HttpResponse:
    """Вернуть страницу со списком документов из data/documents.json."""
    today = date.today()
    documents_list = load_all().documents

    stats = get_documents_statistics(documents_list, today)
    summary = "".join(
        f'<span class="me-3">{status_badge(status)} {count}</span>'
        for status, count in stats.items()
    )

    items = ""
    for document in sort_documents_by_expiry(documents_list):
        status = document.get_status(today)
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/documents/{document.id}/">
                {escape(document.name)} – {escape(document.employee.name)}
            </a>
            <span>до {document.expiry_date} {status_badge(status)}</span>
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Документов пока нет.</li>'

    content = f"""
    <h1>Документы</h1>
    <p>{summary}</p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("HRDocs – документы", content))


# view-функция страницы /documents/<id>/: карточка документа
def document_detail(request: HttpRequest, document_id: int) -> HttpResponse:
    """Вернуть страницу документа или ответ с кодом 404."""
    documents_list = load_all().documents
    document = find_document_by_id(documents_list, document_id)

    if document is None:
        content = """
        <h1 class="text-danger">Документ не найден</h1>
        <a href="/documents/" class="btn btn-outline-secondary">
            ← к списку документов
        </a>
        """
        return HttpResponse(
            page("Документ не найден", content),
            status=404,
        )

    status = document.get_status(date.today())
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(document.name)}</h5>
            <p class="card-text">
                <strong>ID:</strong> {document.id}
            </p>
            <p class="card-text">
                <strong>Категория:</strong> {escape(document.category.name)}
                – {escape(document.category.description)}
            </p>
            <p class="card-text">
                <strong>Сотрудник:</strong>
                <a href="/employees/{document.employee.id}/">
                    {escape(document.employee.name)}
                </a>
            </p>
            <p class="card-text">
                <strong>Срок действия до:</strong> {document.expiry_date}
            </p>
            <p class="card-text">
                <strong>Статус:</strong> {status_badge(status)}
            </p>
            <a href="/documents/" class="btn btn-outline-secondary">
                ← к списку документов
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(escape(document.name), content),
        status=200,
    )
