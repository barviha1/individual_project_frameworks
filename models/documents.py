"""Класс Document и функции работы с коллекцией документов."""
from datetime import date
from typing import Iterator

from .categories import Category
from .employees import Employee


class Document:
    """Кадровый документ, связанный с сотрудником и категорией."""

    def __init__(
        self,
        document_id: int,
        name: str,
        category: Category,
        employee: Employee,
        expiry_date: str,
    ) -> None:
        """Создать объект документа."""
        self.id = document_id
        self.name = name
        self.category = category
        self.employee = employee
        self.expiry_date = expiry_date

    def get_status(self, today: date) -> str:
        """Вернуть текстовый статус документа по сроку действия.

        Метод развивает функцию get_document_status(), реализованную
        в ПР1 и ПР2: теперь она работает с данными самого объекта.
        """
        expiry = date.fromisoformat(self.expiry_date)
        days_left = (expiry - today).days
        if days_left < 0:
            return "Истёк"
        if days_left <= 30:
            return "Скоро истекает"
        return "Активен"

    def to_report_line(self, status: str) -> str:
        """Сформировать строку отчёта по документу.

        Метод развивает функцию generate_report_line() из ПР2.
        """
        title = f"{self.name} ({self.category.name}, {self.employee.name})"
        if status in ("Истёк", "Скоро истекает"):
            return f"[ВНИМАНИЕ] {title}: {status}"
        return f"{title}: {status}"

    def __str__(self) -> str:
        """Вернуть строковое представление документа."""
        return f"{self.name} ({self.category.name}) — {self.employee.name}"


# функция добавления документа с привязкой к сотруднику и категории
def add_document(
    documents: list[Document],
    name: str,
    category: Category,
    employee: Employee,
    expiry_date: str,
) -> Document:
    """Создать объект Document, добавить его в коллекцию и вернуть его."""
    document_id = max((d.id for d in documents), default=0) + 1
    document = Document(document_id, name, category, employee, expiry_date)
    documents.append(document)
    return document


# функция поиска документов конкретного сотрудника
def find_documents_by_employee(
    documents: list[Document], employee: Employee
) -> list[Document]:
    """Вернуть документы, привязанные к указанному сотруднику."""
    return [d for d in documents if d.employee.id == employee.id]


# функция фильтрации документов по категории
def filter_documents_by_category(
    documents: list[Document], category: Category
) -> list[Document]:
    """Отобрать документы указанной категории."""
    return [d for d in documents if d.category.name == category.name]


# функция-генератор: последовательно отдаёт документы с нужным статусом
def iter_documents_by_status(
    documents: list[Document], today: date, status: str
) -> Iterator[Document]:
    """Генератор документов с указанным статусом срока действия."""
    for document in documents:
        if document.get_status(today) == status:
            yield document


# функция сортировки документов по дате истечения срока (lambda-ключ)
def sort_documents_by_expiry(documents: list[Document]) -> list[Document]:
    """Вернуть документы, отсортированные по дате истечения срока."""
    return sorted(documents, key=lambda d: d.expiry_date)


# функция подсчёта статистики документов по статусам срока
def get_documents_statistics(
    documents: list[Document], today: date
) -> dict[str, int]:
    """Подсчитать количество документов по каждому статусу срока действия."""
    stats = {"Активен": 0, "Скоро истекает": 0, "Истёк": 0}
    for document in documents:
        stats[document.get_status(today)] += 1
    return stats
