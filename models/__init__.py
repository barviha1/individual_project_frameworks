"""Пакет с классами предметной области индивидуального проекта."""
from .categories import Category
from .documents import Document
from .employees import Employee

__all__ = ["Employee", "Category", "Document"]
