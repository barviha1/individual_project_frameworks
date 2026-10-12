"""Тесты страницы категорий."""
from unittest.mock import patch

from django.test import SimpleTestCase

from models import Category, Document, Employee
from storage import ProjectData

CONTRACT = Category("Трудовой договор", "Основной документ")
ORDER = Category("Приказ", "Внутренний документ")
EMPLOYEE = Employee(
    1, "Иванов Иван Иванович", "Специалист", "Отдел кадров", "2026-03-30"
)
DOCUMENT = Document(
    1, "Трудовой договор №1", CONTRACT, EMPLOYEE, "2026-09-30"
)


def fake_load_all() -> ProjectData:
    """Вернуть тестовые данные вместо чтения JSON-файлов."""
    return ProjectData([EMPLOYEE], [CONTRACT, ORDER], [DOCUMENT])


@patch("categories.views.load_all", fake_load_all)
class CategoryPagesTests(SimpleTestCase):
    """Проверка страницы /categories/."""

    # тест: список категорий открывается и содержит все категории
    def test_list_page(self) -> None:
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Трудовой договор")
        self.assertContains(response, "Приказ")

    # тест: для каждой категории выводится число её документов
    def test_documents_count(self) -> None:
        response = self.client.get("/categories/")
        self.assertContains(response, "документов: 1")
        self.assertContains(response, "документов: 0")
