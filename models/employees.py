"""Класс Employee и функции работы с коллекцией сотрудников."""
from datetime import date


class Employee:
    """Сотрудник организации."""

    def __init__(
        self,
        employee_id: int,
        name: str,
        position: str,
        department: str,
        hire_date: str,
    ) -> None:
        """Создать объект сотрудника."""
        self.id = employee_id
        self.name = name
        self.position = position
        self.department = department
        self.hire_date = hire_date

    def get_seniority(self, today: date) -> float:
        """Вычислить стаж сотрудника в годах на дату today."""
        hire = date.fromisoformat(self.hire_date)
        days = (today - hire).days
        return round(days / 365, 1)

    def update_info(
        self,
        position: str | None = None,
        department: str | None = None,
    ) -> None:
        """Изменить должность и/или отдел сотрудника."""
        if position:
            self.position = position
        if department:
            self.department = department

    @classmethod
    def from_data(cls, data: dict) -> "Employee":
        """Создать сотрудника из словаря (при загрузке из JSON)."""
        return cls(
            employee_id=data["id"],
            name=data["name"],
            position=data["position"],
            department=data["department"],
            hire_date=data["hire_date"],
        )

    def __str__(self) -> str:
        """Вернуть строковое представление сотрудника."""
        return f"{self.name} — {self.position}, {self.department}"


# функция добавления нового сотрудника в коллекцию
def add_employee(
    employees: list[Employee],
    name: str,
    position: str,
    department: str,
    hire_date: str,
) -> Employee:
    """Создать объект Employee, добавить его в коллекцию и вернуть его."""
    employee_id = max((e.id for e in employees), default=0) + 1
    employee = Employee(employee_id, name, position, department, hire_date)
    employees.append(employee)
    return employee


# функция поиска сотрудника по идентификатору
def find_employee_by_id(
    employees: list[Employee], employee_id: int
) -> Employee | None:
    """Найти сотрудника по идентификатору."""
    for employee in employees:
        if employee.id == employee_id:
            return employee
    return None


# функция поиска сотрудников по подстроке в имени
def find_employee(employees: list[Employee], query: str) -> list[Employee]:
    """Найти сотрудников, чьё имя содержит подстроку query."""
    query = query.lower()
    return [e for e in employees if query in e.name.lower()]


# функция редактирования должности и/или отдела сотрудника
def edit_employee(
    employees: list[Employee],
    employee_id: int,
    position: str | None = None,
    department: str | None = None,
) -> bool:
    """Найти сотрудника и изменить его данные через его собственный метод."""
    employee = find_employee_by_id(employees, employee_id)
    if employee is None:
        return False
    employee.update_info(position, department)
    return True


# функция удаления сотрудника по идентификатору
def delete_employee(employees: list[Employee], employee_id: int) -> bool:
    """Удалить сотрудника из коллекции по идентификатору."""
    employee = find_employee_by_id(employees, employee_id)
    if employee is None:
        return False
    employees.remove(employee)
    return True
