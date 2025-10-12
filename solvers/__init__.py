"""
Пакет solvers - содержит тренажеры и решатели для игры 2048
Включает медленную версию с подтверждением ходов и быструю с автоматическими ходами
"""

from .slow import PracticeSlowUI
from .fast import PracticeFastUI

__all__ = ["PracticeSlowUI", "PracticeFastUI"]
