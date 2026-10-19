"""Тесты страниц сотрудников."""
from unittest.mock import patch

from django.test import SimpleTestCase

from models import Category, Document, Employee
from storage import ProjectData

CATEGORY = Category("Трудовой договор", "Основной документ")
EMPLOYEE = Employee(
    1, "Иванов Иван Иванович", "Специалист", "Отдел кадров", "2026-03-30"
)
DOCUMENT = Document(
    1, "Трудовой договор №1", CATEGORY, EMPLOYEE, "2026-09-30"
)


def fake_load_all() -> ProjectData:
    """Вернуть тестовые данные вместо чтения JSON-файлов."""
    return ProjectData([EMPLOYEE], [CATEGORY], [DOCUMENT])


@patch("employees.views.load_all", fake_load_all)
class EmployeePagesTests(SimpleTestCase):
    """Проверка страниц /employees/ и /employees/<id>/."""

    # тест: список сотрудников открывается и содержит сотрудника
    def test_list_page(self) -> None:
        response = self.client.get("/employees/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Иванов Иван Иванович")
        self.assertContains(response, 'href="/employees/1/"')

    # тест: страница сотрудника показывает его данные и документы
    def test_detail_page(self) -> None:
        response = self.client.get("/employees/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Специалист")
        self.assertContains(response, "Трудовой договор №1")

    # тест: несуществующий id сотрудника даёт страницу с кодом 404
    def test_detail_page_not_found(self) -> None:
        response = self.client.get("/employees/999/")
        self.assertContains(response, "Сотрудник не найден", status_code=404)

    # тест: страницы строятся из шаблонов, карточка подключена через include
    def test_templates_used(self) -> None:
        response = self.client.get("/employees/")
        self.assertTemplateUsed(response, "employees/employee_list.html")
        self.assertTemplateUsed(
            response, "employees/includes/employee_card.html"
        )

    # тест: фильтр length выводит число сотрудников
    def test_length_filter(self) -> None:
        response = self.client.get("/employees/")
        self.assertContains(response, "Всего сотрудников: 1")

    # тест: фильтр date выводит дату приёма в формате дд.мм.гггг
    def test_date_filter(self) -> None:
        response = self.client.get("/employees/1/")
        self.assertContains(response, "30.03.2026")

    # тест: при пустом списке срабатывает {% empty %}
    def test_empty_list(self) -> None:
        empty = ProjectData([], [], [])
        with patch("employees.views.load_all", lambda: empty):
            response = self.client.get("/employees/")
        self.assertContains(response, "Сотрудников пока нет.")

    # тест: HTML-теги в данных экранируются и не попадают на страницу
    def test_name_is_escaped(self) -> None:
        evil = Employee(
            2, "<script>x</script>", "Должность", "Отдел", "2026-01-01"
        )
        data = ProjectData([evil], [CATEGORY], [])
        with patch("employees.views.load_all", lambda: data):
            response = self.client.get("/employees/")
        self.assertNotContains(response, "<script>")
        self.assertContains(response, "&lt;script&gt;")
