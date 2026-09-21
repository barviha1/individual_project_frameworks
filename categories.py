"""Функции управления категориями документов."""


# функция создания новой категории документа
def add_category(
    categories: dict[str, str], name: str, description: str
) -> None:
    """Создать новую категорию документа.

    Если категория с таким названием уже существует,
    её описание будет перезаписано.
    """
    categories[name] = description


# функция редактирования описания категории
def edit_category(
    categories: dict[str, str], name: str, new_description: str
) -> bool:
    """Изменить описание существующей категории.

    Возвращает True, если категория найдена и обновлена, иначе False.
    """
    if name not in categories:
        return False
    categories[name] = new_description
    return True


# функция удаления категории
def delete_category(categories: dict[str, str], name: str) -> bool:
    """Удалить категорию по названию.

    Возвращает True, если категория была удалена, иначе False.
    """
    if name not in categories:
        return False
    del categories[name]
    return True


# функция получения описания категории (для отображения документа)
def get_category_label(categories: dict[str, str], category: str) -> str:
    """Вернуть описание категории.

    Если категория отсутствует в справочнике, возвращается
    значение по умолчанию.
    """
    return categories.get(category, "Прочий кадровый документ")


# функция получения списка всех категорий (для меню)
def list_categories(categories: dict[str, str]) -> list[str]:
    """Вернуть отсортированный по названию список категорий."""
    return sorted(categories.keys())
