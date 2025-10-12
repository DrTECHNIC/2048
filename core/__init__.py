"""
Пакет core - содержит основную логику игры 2048
"""

from .base import BaseGame2048
from .normal import NormalGame2048
from .easy import EasyGame2048
from .hard import HardGame2048

__all__ = ["BaseGame2048", "NormalGame2048", "EasyGame2048", "HardGame2048"]
