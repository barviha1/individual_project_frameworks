"""Тесты класса Document и функций работы с документами."""
from datetime import date

from models.categories import Category
from models.documents import (
    add_document,
    filter_documents_by_category,
    find_document_by_id,
    find_documents_by_employee,
    get_documents_statistics,
    sort_documents_by_expiry,
)
from models.employees import Employee

CONTRACT = Category("Трудовой договор", "Основной документ")
ORDER = Category("Приказ", "Внутренний документ")
EMPLOYEE = Employee(
    1, "Иванов Иван Иванович", "Специалист", "Отдел кадров", "2026-03-30"
)
EMPLOYEE_2 = Employee(
    2, "Петрова Анна Сергеевна", "HR-менеджер", "Отдел кадров", "2025-01-10"
)


# тест: добавление документа создаёт объект и связывает его с сотрудником
def test_add_document():
    documents = []
    document = add_document(
        documents, "Трудовой договор №1", CONTRACT, EMPLOYEE, "2026-09-30"
    )
    assert document.id == 1
    assert document.employee is EMPLOYEE
    assert len(documents) == 1


# тест: поиск документов конкретного сотрудника отбирает только его
def test_find_documents_by_employee():
    documents = []
    add_document(
        documents, "Трудовой договор №1", CONTRACT, EMPLOYEE, "2026-09-30"
    )
    add_document(documents, "Приказ №5", ORDER, EMPLOYEE_2, "2026-12-01")
    found = find_documents_by_employee(documents, EMPLOYEE)
    assert len(found) == 1
    assert found[0].employee.id == EMPLOYEE.id


# тест: фильтрация по категории отбирает только нужные документы
def test_filter_documents_by_category():
    documents = []
    add_document(
        documents, "Трудовой договор №1", CONTRACT, EMPLOYEE, "2026-09-30"
    )
    add_document(documents, "Приказ №5", ORDER, EMPLOYEE, "2026-12-01")
    found = filter_documents_by_category(documents, ORDER)
    assert len(found) == 1
    assert found[0].category.name == "Приказ"


# тест: статус документа верно определяется методом get_status
def test_get_document_status():
    today = date(2026, 9, 12)
    expired = add_document([], "Справка №1", CONTRACT, EMPLOYEE, "2026-09-01")
    soon = add_document([], "Справка №2", CONTRACT, EMPLOYEE, "2026-09-30")
    active = add_document([], "Справка №3", CONTRACT, EMPLOYEE, "2027-01-01")
    assert expired.get_status(today) == "Истёк"
    assert soon.get_status(today) == "Скоро истекает"
    assert active.get_status(today) == "Активен"


# тест: статистика верно считает документы по статусам
def test_get_documents_statistics():
    documents = []
    add_document(
        documents, "Трудовой договор №1", CONTRACT, EMPLOYEE, "2026-09-30"
    )
    add_document(documents, "Справка №2", CONTRACT, EMPLOYEE, "2026-09-01")
    stats = get_documents_statistics(documents, date(2026, 9, 12))
    assert stats["Скоро истекает"] == 1
    assert stats["Истёк"] == 1


# тест: сортировка расставляет документы по дате истечения
def test_sort_documents_by_expiry():
    documents = []
    add_document(documents, "Приказ №5", ORDER, EMPLOYEE, "2026-12-01")
    add_document(
        documents, "Трудовой договор №1", CONTRACT, EMPLOYEE, "2026-09-30"
    )
    sorted_docs = sort_documents_by_expiry(documents)
    assert sorted_docs[0].expiry_date == "2026-09-30"


# тест: строка отчёта помечает документы с истекающим или истёкшим сроком
def test_to_report_line():
    document = add_document(
        [], "Справка №1", CONTRACT, EMPLOYEE, "2026-09-01"
    )
    status = document.get_status(date(2026, 9, 12))
    line = document.to_report_line(status)
    assert "[ВНИМАНИЕ]" in line


# тест: поиск документа по id возвращает объект или None
def test_find_document_by_id():
    documents = []
    document = add_document(
        documents, "Приказ №5", ORDER, EMPLOYEE, "2026-12-01"
    )
    assert find_document_by_id(documents, document.id) is document
    assert find_document_by_id(documents, 999) is None
