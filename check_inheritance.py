import sys
import os

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pages.search_page import SearchPage
from pages.base_page import BasePage

print(f"=== ПУТИ ИМПОРТА ===")
print(f"BasePage модуль: {BasePage.__module__}")
print(f"BasePage файл: {BasePage.__module__.replace('.', '/')}.py")
print(f"SearchPage модуль: {SearchPage.__module__}")
print(f"SearchPage базовые классы: {SearchPage.__bases__}")

print(f"\n=== ПРОВЕРКА НАСЛЕДОВАНИЯ ===")
print(f"SearchPage наследуется от BasePage: {issubclass(SearchPage, BasePage)}")
print(f"Метод 'open' есть в SearchPage: {hasattr(SearchPage, 'open')}")
print(f"Метод 'open' есть в BasePage: {hasattr(BasePage, 'open')}")

print(f"\n=== ПРОВЕРКА ЭКЗЕМПЛЯРА ===")
try:
    # Создаём мок-объект драйвера для проверки
    class MockDriver:
        pass


    page = SearchPage(MockDriver())
    print(f"Экземпляр SearchPage создан: {page is not None}")
    print(f"Метод 'open' есть у экземпляра: {hasattr(page, 'open')}")
except Exception as e:
    print(f"Ошибка при создании экземпляра: {e}")