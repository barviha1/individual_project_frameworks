"""Тесты класса Category и функций работы с категориями документов."""
from models.categories import (
    Category,
    add_category,
    delete_category,
    edit_category,
    find_category_by_name,
    list_categories,
)

NAME = "Трудовой договор"
DESCRIPTION = "Основной документ о трудовых отношениях"


# тест: добавление категории создаёт объект с верными атрибутами
def test_add_category():
    categories = []
    category = add_category(categories, NAME, DESCRIPTION)
    assert category.name == NAME
    assert category.description == DESCRIPTION
    assert len(categories) == 1


# тест: поиск категории по названию находит добавленную
def test_find_category_by_name():
    categories = []
    add_category(categories, NAME, DESCRIPTION)
    assert find_category_by_name(categories, NAME) is not None
    assert find_category_by_name(categories, "Приказ") is None


# тест: редактирование меняет описание, несуществующая категория — False
def test_edit_category():
    categories = []
    add_category(categories, NAME, DESCRIPTION)
    assert edit_category(categories, NAME, "Новое описание")
    category = find_category_by_name(categories, NAME)
    assert category.description == "Новое описание"
    assert not edit_category(categories, "Приказ", "Любое")


# тест: удаление убирает категорию, повторное удаление даёт False
def test_delete_category():
    categories = []
    add_category(categories, NAME, DESCRIPTION)
    assert delete_category(categories, NAME)
    assert find_category_by_name(categories, NAME) is None
    assert not delete_category(categories, NAME)


# тест: список названий категорий возвращается отсортированным
def test_list_categories():
    categories = []
    add_category(categories, "Справка", "Информационный документ")
    add_category(categories, "Приказ", "Внутренний документ")
    assert list_categories(categories) == ["Приказ", "Справка"]


# тест: валидатор отклоняет пустое или состоящее из пробелов название
def test_validate_name():
    assert Category.validate_name("Приказ")
    assert not Category.validate_name("   ")
