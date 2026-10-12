"""Тесты страниц документов."""
from unittest.mock import patch

from django.test import SimpleTestCase

from models import Category, Document, Employee
from storage import ProjectData

CATEGORY = Category("Трудовой договор", "Основной документ")
EMPLOYEE = Employee(
    1, "Иванов Иван Иванович", "Специалист", "Отдел кадров", "2026-03-30"
)
EXPIRED = Document(1, "Справка №1", CATEGORY, EMPLOYEE, "2000-01-01")
ACTIVE = Document(2, "Договор №2", CATEGORY, EMPLOYEE, "2999-01-01")


def fake_load_all() -> ProjectData:
    """Вернуть тестовые данные вместо чтения JSON-файлов."""
    return ProjectData([EMPLOYEE], [CATEGORY], [ACTIVE, EXPIRED])


@patch("documents.views.load_all", fake_load_all)
class DocumentPagesTests(SimpleTestCase):
    """Проверка страниц /documents/ и /documents/<id>/."""

    # тест: список документов открывается и содержит оба документа
    def test_list_page(self) -> None:
        response = self.client.get("/documents/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Справка №1")
        self.assertContains(response, "Договор №2")

    # тест: документы в списке упорядочены по сроку действия
    def test_list_sorted_by_expiry(self) -> None:
        html = self.client.get("/documents/").content.decode()
        self.assertLess(html.index("Справка №1"), html.index("Договор №2"))

    # тест: статус документа определяется по сроку (истёк / активен)
    def test_status_badges(self) -> None:
        response = self.client.get("/documents/")
        self.assertContains(response, "bg-danger")
        self.assertContains(response, "bg-success")

    # тест: страница документа показывает связанные объекты
    def test_detail_page(self) -> None:
        response = self.client.get("/documents/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Трудовой договор")
        self.assertContains(response, "Иванов Иван Иванович")
        self.assertContains(response, 'href="/employees/1/"')

    # тест: несуществующий id документа даёт страницу с кодом 404
    def test_detail_page_not_found(self) -> None:
        response = self.client.get("/documents/999/")
        self.assertContains(response, "Документ не найден", status_code=404)
