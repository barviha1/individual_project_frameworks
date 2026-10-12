"""Тесты главной страницы и общего каркаса."""
from django.test import SimpleTestCase

from homepage.views import page, status_badge


class HomepageTests(SimpleTestCase):
    """Проверка страницы / и вспомогательных функций каркаса."""

    # тест: главная страница открывается и содержит ссылки на разделы
    def test_index_page(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HRDocs")
        self.assertContains(response, 'href="/employees/"')
        self.assertContains(response, 'href="/documents/"')

    # тест: каркас page() подключает Bootstrap и задаёт заголовок вкладки
    def test_page_skeleton(self) -> None:
        html = page("Заголовок", "<p>Текст</p>")
        self.assertIn("<title>Заголовок</title>", html)
        self.assertIn("bootstrap", html)
        self.assertIn("<p>Текст</p>", html)

    # тест: цвет бейджа зависит от статуса документа
    def test_status_badge(self) -> None:
        self.assertIn("bg-success", status_badge("Активен"))
        self.assertIn("bg-warning", status_badge("Скоро истекает"))
        self.assertIn("bg-danger", status_badge("Истёк"))

    # тест: несуществующий адрес даёт собственную страницу 404 (handler404)
    def test_unknown_url(self) -> None:
        response = self.client.get("/nonexistent/")
        self.assertContains(
            response, "404 – страница не найдена", status_code=404
        )
        self.assertContains(response, 'href="/"', status_code=404)

    # тест: адрес с неподходящим конвертером <int:...> тоже даёт 404
    def test_bad_converter_url(self) -> None:
        response = self.client.get("/employees/abc/")
        self.assertContains(
            response, "404 – страница не найдена", status_code=404
        )
