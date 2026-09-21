from datetime import date

from employees import (
    add_employee,
    delete_employee,
    edit_employee,
    find_employee,
    get_employee_seniority,
)

NAME = "Иванов Иван Иванович"
POSITION = "Специалист"
DEPARTMENT = "Отдел кадров"
HIRE_DATE = "2026-03-30"


# тест: добавление сотрудника увеличивает словарь и возвращает id
def test_add_employee():
    employees = {}
    employee_id = add_employee(
        employees, NAME, POSITION, DEPARTMENT, HIRE_DATE
    )
    assert employee_id == 1
    assert len(employees) == 1


# тест: поиск сотрудника по части имени находит добавленного
def test_find_employee():
    employees = {}
    add_employee(employees, NAME, POSITION, DEPARTMENT, HIRE_DATE)
    assert find_employee(employees, "иванов")


# тест: редактирование меняет должность, а несуществующий id даёт False
def test_edit_employee():
    employees = {}
    employee_id = add_employee(
        employees, NAME, POSITION, DEPARTMENT, HIRE_DATE
    )
    assert edit_employee(employees, employee_id, position="Ведущий")
    assert employees[employee_id]["position"] == "Ведущий"
    assert not edit_employee(employees, 999)


# тест: удаление убирает сотрудника, повторное удаление даёт False
def test_delete_employee():
    employees = {}
    employee_id = add_employee(
        employees, NAME, POSITION, DEPARTMENT, HIRE_DATE
    )
    assert delete_employee(employees, employee_id)
    assert employee_id not in employees
    assert not delete_employee(employees, employee_id)


# тест: стаж считается верно по разнице дат
def test_get_employee_seniority():
    employee = {"hire_date": "2026-03-30"}
    seniority = get_employee_seniority(employee, date(2026, 9, 12))
    assert seniority == 0.5
