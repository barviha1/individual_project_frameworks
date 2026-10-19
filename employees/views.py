"""View-функции страниц сотрудников."""
from datetime import date
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from documents.views import build_document_rows
from models.documents import find_documents_by_employee
from models.employees import find_employee_by_id
from storage import load_all


# view-функция страницы /employees/: список сотрудников
def employees(request: HttpRequest) -> HttpResponse:
    """Вернуть страницу со списком сотрудников из data/employees.json."""
    today = date.today()
    context = {
        "employee_rows": [
            {
                "employee": employee,
                "seniority": employee.get_seniority(today),
            }
            for employee in load_all().employees
        ],
    }
    return render(request, "employees/employee_list.html", context)


# view-функция страницы /employees/<id>/: карточка сотрудника и его документы
def employee_detail(request: HttpRequest, employee_id: int) -> HttpResponse:
    """Вернуть страницу сотрудника или ответ с кодом 404."""
    data = load_all()
    employee = find_employee_by_id(data.employees, employee_id)

    context: dict[str, Any] = {"employee": employee}
    if employee is not None:
        today = date.today()
        context["seniority"] = employee.get_seniority(today)
        context["hire_date"] = date.fromisoformat(employee.hire_date)
        context["document_rows"] = build_document_rows(
            find_documents_by_employee(data.documents, employee), today
        )

    return render(
        request,
        "employees/employee_detail.html",
        context,
        status=404 if employee is None else 200,
    )
