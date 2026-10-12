"""Тесты класса Employee и функций работы с сотрудниками."""
from datetime import date

from models.employees import (
    add_employee,
    delete_employee,
    edit_employee,
    find_employee,
    find_employee_by_id,
)

NAME = "Иванов Иван Иванович"
POSITION = "Специалист"
DEPARTMENT = "Отдел кадров"
HIRE_DATE = "2026-03-30"


# тест: добавление сотрудника создаёт объект с верными атрибутами
def test_add_employee():
    employees = []
    employee = add_employee(
        employees, NAME, POSITION, DEPARTMENT, HIRE_DATE
    )
    assert employee.id == 1
    assert employee.name == NAME
    assert len(employees) == 1


# тест: поиск сотрудника по части имени находит добавленного
def test_find_employee():
    employees = []
    add_employee(employees, NAME, POSITION, DEPARTMENT, HIRE_DATE)
    assert find_employee(employees, "иванов")


# тест: редактирование меняет должность, а несуществующий id даёт False
def test_edit_employee():
    employees = []
    employee = add_employee(
        employees, NAME, POSITION, DEPARTMENT, HIRE_DATE
    )
    assert edit_employee(employees, employee.id, position="Ведущий")
    assert employee.position == "Ведущий"
    assert not edit_employee(employees, 999)


# тест: удаление убирает сотрудника, повторное удаление даёт False
def test_delete_employee():
    employees = []
    employee = add_employee(
        employees, NAME, POSITION, DEPARTMENT, HIRE_DATE
    )
    assert delete_employee(employees, employee.id)
    assert employee not in employees
    assert not delete_employee(employees, employee.id)


# тест: стаж считается верно по разнице дат
def test_get_employee_seniority():
    employee = add_employee([], NAME, POSITION, DEPARTMENT, HIRE_DATE)
    seniority = employee.get_seniority(date(2026, 9, 12))
    assert seniority == 0.5


# тест: строковое представление содержит должность и отдел
def test_employee_str():
    employee = add_employee([], NAME, POSITION, DEPARTMENT, HIRE_DATE)
    text = str(employee)
    assert POSITION in text
    assert DEPARTMENT in text


# тест: поиск сотрудника по id возвращает объект или None
def test_find_employee_by_id():
    employees = []
    employee = add_employee(
        employees, NAME, POSITION, DEPARTMENT, HIRE_DATE
    )
    assert find_employee_by_id(employees, employee.id) is employee
    assert find_employee_by_id(employees, 999) is None
