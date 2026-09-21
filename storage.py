"""Сохранение и загрузка данных проекта в формате JSON."""
import json


# функция загрузки сотрудников из JSON-файла (с обработкой ошибок)
def load_employees(filename: str) -> dict[int, dict]:
    """Загрузить сотрудников из JSON-файла.

    При отсутствии файла или повреждённом JSON возвращается
    пустой словарь, а пользователю выводится предупреждение.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные сотрудников не загружены.")
        return {}
    return {int(key): value for key, value in raw.items()}


# функция сохранения сотрудников в JSON-файл
def save_employees(filename: str, employees: dict[int, dict]) -> None:
    """Сохранить сотрудников в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(employees, f, ensure_ascii=False, indent=2)


# функция загрузки документов из JSON-файла (с обработкой ошибок)
def load_documents(filename: str) -> list[dict]:
    """Загрузить документы из JSON-файла.

    При отсутствии файла или повреждённом JSON возвращается
    пустой список, а пользователю выводится предупреждение.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные документов не загружены.")
        return []


# функция сохранения документов в JSON-файл
def save_documents(filename: str, documents: list[dict]) -> None:
    """Сохранить документы в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)


# функция загрузки категорий из JSON-файла (с обработкой ошибок)
def load_categories(filename: str) -> dict[str, str]:
    """Загрузить категории документов из JSON-файла.

    При отсутствии файла или повреждённом JSON возвращается
    пустой словарь, а пользователю выводится предупреждение.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные категорий не загружены.")
        return {}


# функция сохранения категорий в JSON-файл
def save_categories(filename: str, categories: dict[str, str]) -> None:
    """Сохранить категории документов в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
