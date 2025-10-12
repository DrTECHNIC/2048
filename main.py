#!/usr/bin/env python3
"""
Главный файл запуска для 2048 Game Collection
Предоставляет единую точку входа во все версии игры через главный хаб
"""

import sys
import os

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__)))

from hubs.main_hub import MainHub  # noqa: E402

if __name__ == "__main__":
    """
    Точка входа в приложение
    Запускает главный хаб для выбора версий игры
    """
    print("Запуск 2048 Game Collection...")
    hub = MainHub()
    hub.run()
