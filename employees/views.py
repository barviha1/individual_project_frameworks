"""View-функции страниц сотрудников."""
from datetime import date

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page, status_badge
from models.documents import find_documents_by_employee
from models.employees import find_employee_by_id
from storage import load_all


# view-функция страницы /employees/: список сотрудников
def employees(request: HttpRequest) -> HttpResponse:
    """Вернуть страницу со списком сотрудников из data/employees.json."""
    today = date.today()
    items = ""
    for employee in load_all().employees:
        text = (
            f"{escape(employee.name)} – {escape(employee.position)}, "
            f"{escape(employee.department)}"
        )
        seniority = employee.get_seniority(today)
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/employees/{employee.id}/">{text}</a>
            <span class="badge bg-light text-dark">
                стаж {seniority} лет
            </span>
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Сотрудников пока нет.</li>'
    content = f"""
    <h1>Сотрудники</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("HRDocs – сотрудники", content))


# view-функция страницы /employees/<id>/: карточка сотрудника и его документы
def employee_detail(request: HttpRequest, employee_id: int) -> HttpResponse:
    """Вернуть страницу сотрудника или ответ с кодом 404."""
    data = load_all()
    employee = find_employee_by_id(data.employees, employee_id)

    if employee is None:
        content = """
        <h1 class="text-danger">Сотрудник не найден</h1>
        <a href="/employees/" class="btn btn-outline-secondary">
            ← к списку сотрудников
        </a>
        """
        return HttpResponse(
            page("Сотрудник не найден", content),
            status=404,
        )

    today = date.today()
    items = ""
    for document in find_documents_by_employee(data.documents, employee):
        status = document.get_status(today)
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/documents/{document.id}/">
                {escape(document.name)} ({escape(document.category.name)})
            </a>
            <span>до {document.expiry_date} {status_badge(status)}</span>
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Документов пока нет.</li>'

    content = f"""
    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">{escape(employee.name)}</h5>
            <p class="card-text">
                <strong>ID:</strong> {employee.id}
            </p>
            <p class="card-text">
                <strong>Должность:</strong> {escape(employee.position)}
            </p>
            <p class="card-text">
                <strong>Отдел:</strong> {escape(employee.department)}
            </p>
            <p class="card-text">
                <strong>Дата приёма:</strong> {employee.hire_date}
            </p>
            <p class="card-text">
                <strong>Стаж:</strong> {employee.get_seniority(today)} лет
            </p>
            <a href="/employees/" class="btn btn-outline-secondary">
                ← к списку сотрудников
            </a>
        </div>
    </div>
    <h2 class="h4">Документы сотрудника</h2>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(
        page(escape(employee.name), content),
        status=200,
    )
