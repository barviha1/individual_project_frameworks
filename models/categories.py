"""Класс Category и функции работы с коллекцией категорий документов."""


class Category:
    """Категория кадрового документа."""

    def __init__(self, name: str, description: str) -> None:
        """Создать объект категории."""
        self.name = name
        self.description = description

    def update_description(self, description: str) -> None:
        """Изменить описание категории."""
        self.description = description

    @staticmethod
    def validate_name(name: str) -> bool:
        """Проверить, что название категории не пустое.

        Используется перед созданием категории, чтобы не допустить
        категорию с пустым или состоящим из пробелов названием.
        """
        return bool(name.strip())

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """Создать категорию из словаря (при загрузке из JSON)."""
        return cls(name=data["name"], description=data["description"])

    def __str__(self) -> str:
        """Вернуть строковое представление категории."""
        return f"{self.name} — {self.description}"


# функция создания категории и добавления её в коллекцию
def add_category(
    categories: list[Category], name: str, description: str
) -> Category:
    """Создать объект Category и добавить его в коллекцию."""
    category = Category(name, description)
    categories.append(category)
    return category


# функция поиска категории по названию
def find_category_by_name(
    categories: list[Category], name: str
) -> Category | None:
    """Найти категорию по точному названию."""
    for category in categories:
        if category.name == name:
            return category
    return None


# функция редактирования описания категории
def edit_category(
    categories: list[Category], name: str, new_description: str
) -> bool:
    """Найти категорию и изменить её описание через собственный метод."""
    category = find_category_by_name(categories, name)
    if category is None:
        return False
    category.update_description(new_description)
    return True


# функция удаления категории по названию
def delete_category(categories: list[Category], name: str) -> bool:
    """Удалить категорию из коллекции по названию."""
    category = find_category_by_name(categories, name)
    if category is None:
        return False
    categories.remove(category)
    return True


# функция получения списка названий всех категорий (для меню)
def list_categories(categories: list[Category]) -> list[str]:
    """Вернуть отсортированный список названий категорий."""
    return sorted(category.name for category in categories)
