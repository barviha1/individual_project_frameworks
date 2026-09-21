"""Функции работы с сотрудниками."""
from datetime import date


# функция добавления нового сотрудника
def add_employee(
    employees: dict[int, dict],
    name: str,
    position: str,
    department: str,
    hire_date: str,
) -> int:
    """Добавить нового сотрудника в словарь employees.

    Идентификатор формируется автоматически. Возвращает
    идентификатор добавленного сотрудника.
    """
    employee_id = max(employees.keys(), default=0) + 1
    employees[employee_id] = {
        "id": employee_id,
        "name": name,
        "position": position,
        "department": department,
        "hire_date": hire_date,
    }
    return employee_id


# функция редактирования должности и/или отдела сотрудника
def edit_employee(
    employees: dict[int, dict],
    employee_id: int,
    position: str | None = None,
    department: str | None = None,
) -> bool:
    """Изменить должность и/или отдел сотрудника.

    Пустые значения (None) означают, что соответствующее поле
    не изменяется. Возвращает True при успешном редактировании,
    иначе False (сотрудник не найден).
    """
    if employee_id not in employees:
        return False
    if position:
        employees[employee_id]["position"] = position
    if department:
        employees[employee_id]["department"] = department
    return True


# функция удаления сотрудника по идентификатору
def delete_employee(employees: dict[int, dict], employee_id: int) -> bool:
    """Удалить сотрудника по идентификатору.

    Возвращает True, если сотрудник был удалён, иначе False.
    """
    if employee_id not in employees:
        return False
    del employees[employee_id]
    return True


# функция поиска сотрудников по подстроке в имени
def find_employee(employees: dict[int, dict], query: str) -> list[dict]:
    """Найти сотрудников, чьё имя содержит подстроку query."""
    query = query.lower()
    return [
        employee
        for employee in employees.values()
        if query in employee["name"].lower()
    ]


# функция расчёта стажа сотрудника в годах (перенесена и развита из ПР1)
def get_employee_seniority(employee: dict, today: date) -> float:
    """Вычислить стаж сотрудника в годах на дату today.

    Функция развивает расчёт стажа, впервые реализованный в ПР1.
    """
    hire = date.fromisoformat(employee["hire_date"])
    days = (today - hire).days
    return round(days / 365, 1)
