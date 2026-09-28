"""Точка запуска приложения «Система управления кадровыми документами»."""
from datetime import date

from models import Category, Document, Employee
from models.categories import (
    add_category,
    delete_category,
    edit_category,
    find_category_by_name,
    list_categories,
)
from models.documents import (
    add_document,
    filter_documents_by_category,
    find_documents_by_employee,
    get_documents_statistics,
    iter_documents_by_status,
    sort_documents_by_expiry,
)
from models.employees import (
    add_employee,
    delete_employee,
    edit_employee,
    find_employee,
    find_employee_by_id,
)
from storage import (
    load_categories,
    load_documents,
    load_employees,
    save_categories,
    save_documents,
    save_employees,
)
from utils import input_date, input_int, input_nonempty, input_optional

EMPLOYEES_FILE = "data/employees.json"
DOCUMENTS_FILE = "data/documents.json"
CATEGORIES_FILE = "data/categories.json"

MENU = """
=== Система управления кадровыми документами ===
1. Показать сотрудников
2. Добавить сотрудника
3. Найти сотрудника по имени
4. Редактировать сотрудника
5. Удалить сотрудника
6. Показать документы
7. Добавить документ
8. Найти документы сотрудника
9. Найти документы по категории
10. Показать статистику по срокам действия
11. Управление категориями
0. Выход
"""


# функция вывода списка сотрудников на экран
def show_employees(employees: list[Employee], today: date) -> None:
    """Вывести список сотрудников вместе со стажем."""
    if not employees:
        print("Список сотрудников пуст.")
        return
    for employee in employees:
        seniority = employee.get_seniority(today)
        print(f"[{employee.id}] {employee} (стаж {seniority} лет)")


# функция вывода списка документов на экран
def show_documents(documents: list[Document], today: date) -> None:
    """Вывести документы с сотрудником, категорией и статусом срока."""
    if not documents:
        print("Документы не найдены.")
        return
    for document in sort_documents_by_expiry(documents):
        status = document.get_status(today)
        print(f"[{document.id}] {document.to_report_line(status)}")


# функция вывода статистики по документам и срокам их действия
def show_statistics(documents: list[Document], today: date) -> None:
    """Вывести статистику и список документов с истекающим сроком."""
    stats = get_documents_statistics(documents, today)
    print("Статистика по документам:")
    for status, count in stats.items():
        print(f"  {status}: {count}")

    print("Документы, у которых срок скоро истекает:")
    expiring = list(
        iter_documents_by_status(documents, today, "Скоро истекает")
    )
    if not expiring:
        print("  таких документов нет.")
    for document in expiring:
        print(f"  [{document.id}] {document} (до {document.expiry_date})")


# функция подменю управления категориями (создание/редактирование/удаление)
def manage_categories(categories: list[Category]) -> None:
    """Подменю создания, редактирования и удаления категорий."""
    existing = ", ".join(list_categories(categories)) or "нет категорий"
    print(f"Категории: {existing}")
    prompt = "Действие (add / edit / delete / cancel): "
    action = input_nonempty(prompt).lower()

    if action == "add":
        name = input_nonempty("Название категории: ")
        if not Category.validate_name(name):
            print("Название категории не может быть пустым.")
            return
        description = input_nonempty("Описание категории: ")
        add_category(categories, name, description)
        print("Категория добавлена.")
    elif action == "edit":
        name = input_nonempty("Название категории: ")
        description = input_nonempty("Новое описание: ")
        if edit_category(categories, name, description):
            print("Категория обновлена.")
        else:
            print("Категория не найдена.")
    elif action == "delete":
        name = input_nonempty("Название категории: ")
        if delete_category(categories, name):
            print("Категория удалена.")
        else:
            print("Категория не найдена.")
    else:
        print("Отменено.")


# функция пользовательского сценария создания документа
def create_new_document(
    documents: list[Document],
    categories: list[Category],
    employees: list[Employee],
) -> None:
    """Найти сотрудника и категорию и создать связанный документ."""
    employee_id = input_int("Id сотрудника: ")
    employee = find_employee_by_id(employees, employee_id)
    if employee is None:
        print("Сотрудник с таким id не найден.")
        return

    category_name = input_nonempty("Категория: ")
    category = find_category_by_name(categories, category_name)
    if category is None:
        print("Категория не найдена. Сначала создайте её в пункте 11.")
        return

    name = input_nonempty("Название документа: ")
    expiry_date = input_date("Срок действия (дд.мм.гггг): ")
    document = add_document(
        documents, name, category, employee, expiry_date.isoformat()
    )
    print(f"Документ добавлен, id = {document.id}")


# функция точки входа: цикл меню и обработка выбора пользователя
def main() -> None:
    """Основной цикл меню приложения."""
    employees = load_employees(EMPLOYEES_FILE)
    categories = load_categories(CATEGORIES_FILE)
    documents = load_documents(DOCUMENTS_FILE, categories, employees)
    today = date.today()

    while True:
        print(MENU)
        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_employees(employees, today)
        elif choice == 2:
            name = input_nonempty("ФИО сотрудника: ")
            position = input_nonempty("Должность: ")
            department = input_nonempty("Отдел: ")
            hire_date = input_date("Дата приёма (дд.мм.гггг): ")
            employee = add_employee(
                employees, name, position, department, hire_date.isoformat()
            )
            print(f"Сотрудник добавлен, id = {employee.id}")
        elif choice == 3:
            query = input_nonempty("Часть имени для поиска: ")
            found = find_employee(employees, query)
            if not found:
                print("Сотрудники не найдены.")
            for employee in found:
                print(f"[{employee.id}] {employee}")
        elif choice == 4:
            employee_id = input_int("Id сотрудника: ")
            position = input_optional("Новая должность (Enter — не менять): ")
            department = input_optional("Новый отдел (Enter — не менять): ")
            updated = edit_employee(
                employees, employee_id, position or None, department or None
            )
            if updated:
                print("Данные сотрудника обновлены.")
            else:
                print("Сотрудник не найден.")
        elif choice == 5:
            employee_id = input_int("Id сотрудника: ")
            deleted = delete_employee(employees, employee_id)
            if deleted:
                print("Сотрудник удалён.")
            else:
                print("Сотрудник не найден.")
        elif choice == 6:
            show_documents(documents, today)
        elif choice == 7:
            create_new_document(documents, categories, employees)
        elif choice == 8:
            employee_id = input_int("Id сотрудника: ")
            employee = find_employee_by_id(employees, employee_id)
            if employee is None:
                print("Сотрудник с таким id не найден.")
            else:
                found = find_documents_by_employee(documents, employee)
                show_documents(found, today)
        elif choice == 9:
            category_name = input_nonempty("Категория: ")
            category = find_category_by_name(categories, category_name)
            if category is None:
                print("Категория не найдена.")
            else:
                found = filter_documents_by_category(documents, category)
                show_documents(found, today)
        elif choice == 10:
            show_statistics(documents, today)
        elif choice == 11:
            manage_categories(categories)
        elif choice == 0:
            save_employees(EMPLOYEES_FILE, employees)
            save_categories(CATEGORIES_FILE, categories)
            save_documents(DOCUMENTS_FILE, documents)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
