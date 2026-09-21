"""Вспомогательные функции для безопасного ввода данных."""
from datetime import date


# функция безопасного ввода целого числа (повтор при ошибке)
def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число, повторяя запрос при ошибке."""
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Введите целое число.")


# функция безопасного ввода даты дд.мм.гггг (повтор при ошибке)
def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате дд.мм.гггг."""
    while True:
        raw = input(prompt)
        try:
            day, month, year = (int(part) for part in raw.split("."))
            return date(year, month, day)
        except ValueError:
            print("Введите дату в формате дд.мм.гггг, например 15.09.2026.")


# функция безопасного ввода непустой строки (повтор при ошибке)
def input_nonempty(prompt: str) -> str:
    """Запросить у пользователя непустую строку, повторяя запрос при ошибке."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Значение не может быть пустым.")


# функция ввода строки, которую можно оставить пустой (для редактирования)
def input_optional(prompt: str) -> str:
    """Запросить строку, которую можно оставить пустой.

    Используется, например, при редактировании: пустой ответ
    означает, что поле не нужно менять.
    """
    return input(prompt).strip()
