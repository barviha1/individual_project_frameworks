"""Точка запуска приложения «Система управления кадровыми документами»."""
from datetime import date

from categories import (
    add_category,
    delete_category,
    edit_category,
    get_category_label,
    list_categories,
)
from documents import (
    add_document,
    filter_documents_by_category,
    find_documents_by_employee,
    generate_report_line,
    get_document_status,
    get_documents_statistics,
    iter_documents_by_status,
    sort_documents_by_expiry,
)
from employees import (
    add_employee,
    delete_employee,
    edit_employee,
    find_employee,
    get_employee_seniority,
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
def show_employees(employees: dict[int, dict], today: date) -> None:
    """Вывести список сотрудников вместе со стажем."""
    if not employees:
        print("Список сотрудников пуст.")
        return
    for employee in employees.values():
        seniority = get_employee_seniority(employee, today)
        print(
            f"[{employee['id']}] {employee['name']} — "
            f"{employee['position']}, {employee['department']} "
            f"(принят {employee['hire_date']}, стаж {seniority} лет)"
        )


# функция вывода списка документов на экран
def show_documents(
    documents: list[dict],
    employees: dict[int, dict],
    categories: dict[str, str],
    today: date,
) -> None:
    """Вывести документы с сотрудником, категорией и статусом срока."""
    if not documents:
        print("Документы не найдены.")
        return
    for doc in sort_documents_by_expiry(documents):
        employee = employees.get(doc["employee_id"])
        employee_name = employee["name"] if employee else "не найден"
        expiry = date.fromisoformat(doc["expiry_date"])
        status = get_document_status(expiry, today)
        label = get_category_label(categories, doc["category"])
        title = (
            f"[{doc['id']}] {doc['name']} "
            f"({doc['category']} — {label}, {employee_name})"
        )
        print(generate_report_line(title, status))


# функция вывода статистики по документам и срокам их действия
def show_statistics(documents: list[dict], today: date) -> None:
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
    for doc in expiring:
        print(f"  [{doc['id']}] {doc['name']} (до {doc['expiry_date']})")


# функция подменю управления категориями (создание/редактирование/удаление)
def manage_categories(categories: dict[str, str]) -> None:
    """Подменю создания, редактирования и удаления категорий."""
    existing = ", ".join(list_categories(categories)) or "нет категорий"
    print(f"Категории: {existing}")
    prompt = "Действие (add / edit / delete / cancel): "
    action = input_nonempty(prompt).lower()

    if action == "add":
        name = input_nonempty("Название категории: ")
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


# функция точки входа: цикл меню и обработка выбора пользователя
def main() -> None:
    """Основной цикл меню приложения."""
    employees = load_employees(EMPLOYEES_FILE)
    documents = load_documents(DOCUMENTS_FILE)
    categories = load_categories(CATEGORIES_FILE)
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
            employee_id = add_employee(
                employees, name, position, department, hire_date.isoformat()
            )
            print(f"Сотрудник добавлен, id = {employee_id}")
        elif choice == 3:
            query = input_nonempty("Часть имени для поиска: ")
            found = find_employee(employees, query)
            if not found:
                print("Сотрудники не найдены.")
            for employee in found:
                print(f"[{employee['id']}] {employee['name']}")
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
            print("Сотрудник удалён." if deleted else "Сотрудник не найден.")
        elif choice == 6:
            show_documents(documents, employees, categories, today)
        elif choice == 7:
            employee_id = input_int("Id сотрудника: ")
            if employee_id not in employees:
                print("Сотрудник с таким id не найден.")
            else:
                name = input_nonempty("Название документа: ")
                category = input_nonempty("Категория: ")
                expiry_date = input_date("Срок действия (дд.мм.гггг): ")
                document_id = add_document(
                    documents, name, category,
                    employee_id, expiry_date.isoformat(),
                )
                print(f"Документ добавлен, id = {document_id}")
        elif choice == 8:
            employee_id = input_int("Id сотрудника: ")
            found = find_documents_by_employee(documents, employee_id)
            show_documents(found, employees, categories, today)
        elif choice == 9:
            category = input_nonempty("Категория: ")
            found = filter_documents_by_category(documents, category)
            show_documents(found, employees, categories, today)
        elif choice == 10:
            show_statistics(documents, today)
        elif choice == 11:
            manage_categories(categories)
        elif choice == 0:
            save_employees(EMPLOYEES_FILE, employees)
            save_documents(DOCUMENTS_FILE, documents)
            save_categories(CATEGORIES_FILE, categories)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
