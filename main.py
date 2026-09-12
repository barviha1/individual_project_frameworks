from datetime import date

employee_name = "Иванов Иван Иванович"
employee_position = "Специалист по кадровому делопроизводству"
employee_department = "Отдел кадров"
hire_date = date(2026, 3, 30)

document_name = "Трудовой договор №1"
document_category = "Трудовой договор"
document_expiry_date = date(2026, 9, 30)
today = date(2026, 9, 12)

target_category = "Приказ"  # категория, по которой будем искать документ


# функция добавления сотрудника
def add_employee(name, position, department, hire_date):
    return (f"Сотрудник {name} ({position}, {department}) добавлен в систему. "
            f"Дата приёма: {hire_date}")


# функция добавления документа с привязкой к сотруднику и категории
def add_document(doc_name, category, expiry_date, employee_name):
    return (f"Документ '{doc_name}' категории '{category}' добавлен "
            f"для сотрудника {employee_name}. Срок действия до {expiry_date}")


# функция управления категориями
def get_category_label(category):
    if category == "Трудовой договор":
        return "Основной документ о трудовых отношениях"
    elif category == "Приказ":
        return "Внутренний распорядительный документ"
    elif category == "Справка":
        return "Информационно-подтверждающий документ"
    else:
        return "Прочий кадровый документ"


# функция отслеживания срока действия документа
def get_document_status(expiry_date, today):
    days_left = (expiry_date - today).days  # операция вычитания дат
    if days_left < 0:
        return "Истёк"
    elif days_left <= 30:
        return "Скоро истекает"
    else:
        return "Активен"


# функция поиска и фильтрации документов по категории
def search_by_category(doc_category, target_category):
    if doc_category == target_category:
        return "Документ найден по заданной категории"
    else:
        return "Документ не соответствует заданной категории"


# функция формирования отчёта
def generate_report_line(doc_name, status):
    if status == "Истёк" or status == "Скоро истекает":
        return f"[ВНИМАНИЕ] {doc_name}: {status}"
    else:
        return f"{doc_name}: {status}"


# расчёт стажа сотрудника
seniority_days = (today - hire_date).days
seniority_years = round(seniority_days / 365, 1)  # деление, преобразование в float
seniority_years_str = str(seniority_years)  # преобразование float -> str

# вывод результатов
print(add_employee(employee_name, employee_position, employee_department, hire_date))
print(f"Стаж сотрудника: {seniority_years_str} лет")
print()

print(add_document(document_name, document_category, document_expiry_date, employee_name))
print(f"Тип документа: {get_category_label(document_category)}")

status = get_document_status(document_expiry_date, today)
print(f"Статус документа: {status}")
print()

print(search_by_category(document_category, target_category))
print()

print("Отчёт по документу:")
print(generate_report_line(document_name, status))