"""Тесты страниц документов."""
from unittest.mock import patch

from django.template.loader import render_to_string
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

    # тест: статус выводится включаемым шаблоном document_status.html
    def test_status_include_used(self) -> None:
        response = self.client.get("/documents/")
        self.assertTemplateUsed(response, "documents/document_list.html")
        self.assertTemplateUsed(
            response, "documents/includes/document_status.html"
        )

    # тест: фильтр date выводит срок действия в формате дд.мм.гггг
    def test_date_filter(self) -> None:
        response = self.client.get("/documents/1/")
        self.assertContains(response, "01.01.2000")

    # тест: при пустом списке срабатывает {% empty %}
    def test_empty_list(self) -> None:
        empty = ProjectData([], [], [])
        with patch("documents.views.load_all", lambda: empty):
            response = self.client.get("/documents/")
        self.assertContains(response, "Документов пока нет.")

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


class DocumentStatusTemplateTests(SimpleTestCase):
    """Проверка включаемого шаблона document_status.html."""

    # тест: для каждого статуса выводится бейдж своего цвета
    def test_status_colors(self) -> None:
        template = "documents/includes/document_status.html"
        expected = {
            "Активен": "bg-success",
            "Скоро истекает": "bg-warning",
            "Истёк": "bg-danger",
        }
        for status, css_class in expected.items():
            html = render_to_string(template, {"status": status})
            self.assertIn(css_class, html)
            self.assertIn(status, html)

    # тест: неизвестный статус выводится нейтральным бейджем
    def test_unknown_status(self) -> None:
        template = "documents/includes/document_status.html"
        html = render_to_string(template, {"status": "Неизвестно"})
        self.assertIn("bg-secondary", html)
