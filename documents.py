"""Функции работы с документами и сроками их действия."""
from datetime import date
from typing import Iterator


# функция добавления документа с привязкой к сотруднику и категории
def add_document(
    documents: list[dict],
    name: str,
    category: str,
    employee_id: int,
    expiry_date: str,
) -> int:
    """Добавить документ, привязанный к сотруднику и категории.

    Идентификатор формируется автоматически. Возвращает
    идентификатор добавленного документа.
    """
    document_id = max((doc["id"] for doc in documents), default=0) + 1
    documents.append({
        "id": document_id,
        "name": name,
        "category": category,
        "employee_id": employee_id,
        "expiry_date": expiry_date,
    })
    return document_id


# функция поиска документов конкретного сотрудника
def find_documents_by_employee(
    documents: list[dict], employee_id: int
) -> list[dict]:
    """Вернуть документы, привязанные к указанному сотруднику."""
    return [doc for doc in documents if doc["employee_id"] == employee_id]


# функция фильтрации документов по категории
def filter_documents_by_category(
    documents: list[dict], category: str
) -> list[dict]:
    """Отобрать документы указанной категории."""
    return [doc for doc in documents if doc["category"] == category]


# функция определения статуса срока действия документа
def get_document_status(expiry_date: date, today: date) -> str:
    """Вернуть текстовый статус документа по сроку действия.

    Функция перенесена из ПР1 без изменения логики.
    """
    days_left = (expiry_date - today).days
    if days_left < 0:
        return "Истёк"
    if days_left <= 30:
        return "Скоро истекает"
    return "Активен"


# функция-генератор: последовательно отдаёт документы с нужным статусом
def iter_documents_by_status(
    documents: list[dict], today: date, status: str
) -> Iterator[dict]:
    """Генератор документов с указанным статусом срока действия.

    Значения формируются по мере перебора списка documents,
    а не вычисляются заранее целиком.
    """
    for doc in documents:
        expiry = date.fromisoformat(doc["expiry_date"])
        if get_document_status(expiry, today) == status:
            yield doc


# функция сортировки документов по дате истечения срока (lambda-ключ)
def sort_documents_by_expiry(documents: list[dict]) -> list[dict]:
    """Вернуть документы, отсортированные по дате истечения срока."""
    return sorted(documents, key=lambda doc: doc["expiry_date"])


# функция подсчёта статистики документов по статусам срока
def get_documents_statistics(
    documents: list[dict], today: date
) -> dict[str, int]:
    """Подсчитать количество документов по каждому статусу срока."""
    stats = {"Активен": 0, "Скоро истекает": 0, "Истёк": 0}
    for doc in documents:
        expiry = date.fromisoformat(doc["expiry_date"])
        status = get_document_status(expiry, today)
        stats[status] += 1
    return stats


# функция формирования строки отчёта по документу (перенесена из ПР1)
def generate_report_line(doc_name: str, status: str) -> str:
    """Сформировать строку отчёта по документу.

    Функция перенесена из ПР1 без изменения логики.
    """
    if status in ("Истёк", "Скоро истекает"):
        return f"[ВНИМАНИЕ] {doc_name}: {status}"
    return f"{doc_name}: {status}"
