"""
Пакет games - содержит запускаемые файлы различных версий игры 2048
Предоставляет отдельные точки входа для каждой версии игры
"""

from . import normal_game
from . import easy_game
from . import hard_game

__all__ = ["normal_game", "easy_game", "hard_game"]
