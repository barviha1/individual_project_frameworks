"""Сохранение и загрузка объектов проекта в формате JSON."""
import json

from models import Category, Document, Employee
from models.categories import find_category_by_name
from models.employees import find_employee_by_id


# функция загрузки сотрудников из JSON-файла (с обработкой ошибок)
def load_employees(filename: str) -> list[Employee]:
    """Загрузить сотрудников из JSON-файла и создать объекты Employee."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные сотрудников не загружены.")
        return []
    return [Employee.from_data(item) for item in raw]


# функция сохранения сотрудников в JSON-файл
def save_employees(filename: str, employees: list[Employee]) -> None:
    """Сохранить сотрудников в JSON-файл."""
    data = [
        {
            "id": e.id,
            "name": e.name,
            "position": e.position,
            "department": e.department,
            "hire_date": e.hire_date,
        }
        for e in employees
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# функция загрузки категорий из JSON-файла (с обработкой ошибок)
def load_categories(filename: str) -> list[Category]:
    """Загрузить категории из JSON-файла и создать объекты Category."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные категорий не загружены.")
        return []
    return [Category.from_data(item) for item in raw]


# функция сохранения категорий в JSON-файл
def save_categories(filename: str, categories: list[Category]) -> None:
    """Сохранить категории в JSON-файл."""
    data = [
        {"name": c.name, "description": c.description} for c in categories
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# функция загрузки документов из JSON-файла с восстановлением связей
def load_documents(
    filename: str,
    categories: list[Category],
    employees: list[Employee],
) -> list[Document]:
    """Загрузить документы из JSON, связав их с категориями и сотрудниками.

    Документ, для которого не найдена категория или сотрудник,
    в коллекцию не добавляется.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные документов не загружены.")
        return []

    documents = []
    for item in raw:
        category = find_category_by_name(categories, item["category"])
        employee = find_employee_by_id(employees, item["employee_id"])
        if category is None or employee is None:
            print(f"Документ '{item['name']}' пропущен: не найдена связь.")
            continue
        documents.append(
            Document(
                document_id=item["id"],
                name=item["name"],
                category=category,
                employee=employee,
                expiry_date=item["expiry_date"],
            )
        )
    return documents


# функция сохранения документов в JSON-файл
def save_documents(filename: str, documents: list[Document]) -> None:
    """Сохранить документы в JSON-файл, заменив ссылки на идентификаторы."""
    data = [
        {
            "id": d.id,
            "name": d.name,
            "category": d.category.name,
            "employee_id": d.employee.id,
            "expiry_date": d.expiry_date,
        }
        for d in documents
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
