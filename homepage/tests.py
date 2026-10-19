"""Тесты главной страницы, базового шаблона и именованных маршрутов."""
from django.test import SimpleTestCase
from django.urls import reverse

from homepage import views


class HomepageTests(SimpleTestCase):
    """Проверка страницы / и общего шаблона base.html."""

    # тест: главная страница открывается и содержит ссылки на разделы
    def test_index_page(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HRDocs")
        self.assertContains(response, 'href="/employees/"')
        self.assertContains(response, 'href="/documents/"')

    # тест: страница строится из шаблона, унаследованного от base.html
    def test_index_uses_templates(self) -> None:
        response = self.client.get("/")
        self.assertTemplateUsed(response, "homepage/index.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "includes/navigation.html")

    # тест: base.html задаёт заголовок вкладки и подключает Bootstrap
    def test_base_template_layout(self) -> None:
        html = self.client.get("/").content.decode()
        self.assertIn("Главная – HRDocs", html)
        self.assertIn("bootstrap", html)

    # тест: подключены собственные CSS, JavaScript и логотип (static)
    def test_static_files_linked(self) -> None:
        response = self.client.get("/")
        self.assertContains(response, "/static/homepage/css/style.css")
        self.assertContains(response, "/static/homepage/js/main.js")
        self.assertContains(response, "/static/homepage/img/logo.png")

    # тест: функция page() из ПР5 удалена, HTML не строится в Python
    def test_page_function_removed(self) -> None:
        self.assertFalse(hasattr(views, "page"))
        self.assertFalse(hasattr(views, "status_badge"))

    # тест: именованные маршруты с пространствами имён дают верные адреса
    def test_named_urls(self) -> None:
        self.assertEqual(reverse("homepage:index"), "/")
        self.assertEqual(reverse("employees:list"), "/employees/")
        self.assertEqual(
            reverse("employees:detail", args=[1]), "/employees/1/"
        )
        self.assertEqual(reverse("documents:list"), "/documents/")
        self.assertEqual(
            reverse("documents:detail", args=[2]), "/documents/2/"
        )
        self.assertEqual(reverse("categories:list"), "/categories/")

    # тест: несуществующий адрес даёт собственную страницу 404 (handler404)
    def test_unknown_url(self) -> None:
        response = self.client.get("/nonexistent/")
        self.assertContains(
            response, "404 – страница не найдена", status_code=404
        )
        self.assertContains(response, 'href="/"', status_code=404)
        self.assertTemplateUsed(response, "homepage/404.html")

    # тест: адрес с неподходящим конвертером <int:...> тоже даёт 404
    def test_bad_converter_url(self) -> None:
        response = self.client.get("/employees/abc/")
        self.assertContains(
            response, "404 – страница не найдена", status_code=404
        )
