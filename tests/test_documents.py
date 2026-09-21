from datetime import date

from documents import (
    add_document,
    filter_documents_by_category,
    find_documents_by_employee,
    get_document_status,
    get_documents_statistics,
    sort_documents_by_expiry,
)

CONTRACT = "Трудовой договор"


# тест: добавление документа увеличивает список и возвращает id
def test_add_document():
    documents = []
    document_id = add_document(
        documents, "Трудовой договор №1", CONTRACT, 1, "2026-09-30"
    )
    assert document_id == 1
    assert len(documents) == 1


# тест: поиск документов конкретного сотрудника отбирает только его
def test_find_documents_by_employee():
    documents = []
    add_document(documents, "Трудовой договор №1", CONTRACT, 1, "2026-09-30")
    add_document(documents, "Приказ №5", "Приказ", 2, "2026-12-01")
    found = find_documents_by_employee(documents, 1)
    assert len(found) == 1
    assert found[0]["employee_id"] == 1


# тест: фильтрация по категории отбирает только нужные документы
def test_filter_documents_by_category():
    documents = []
    add_document(documents, "Трудовой договор №1", CONTRACT, 1, "2026-09-30")
    add_document(documents, "Приказ №5", "Приказ", 1, "2026-12-01")
    found = filter_documents_by_category(documents, "Приказ")
    assert len(found) == 1
    assert found[0]["category"] == "Приказ"


# тест: статус документа верно определяется по дате истечения
def test_get_document_status():
    today = date(2026, 9, 12)
    assert get_document_status(date(2026, 9, 1), today) == "Истёк"
    assert get_document_status(date(2026, 9, 30), today) == "Скоро истекает"
    assert get_document_status(date(2027, 1, 1), today) == "Активен"


# тест: статистика верно считает документы по статусам
def test_get_documents_statistics():
    documents = []
    add_document(documents, "Трудовой договор №1", CONTRACT, 1, "2026-09-30")
    add_document(documents, "Справка №2", "Справка", 1, "2026-09-01")
    stats = get_documents_statistics(documents, date(2026, 9, 12))
    assert stats["Скоро истекает"] == 1
    assert stats["Истёк"] == 1


# тест: сортировка расставляет документы по дате истечения
def test_sort_documents_by_expiry():
    documents = []
    add_document(documents, "Приказ №5", "Приказ", 1, "2026-12-01")
    add_document(documents, "Трудовой договор №1", CONTRACT, 1, "2026-09-30")
    sorted_docs = sort_documents_by_expiry(documents)
    assert sorted_docs[0]["expiry_date"] == "2026-09-30"
