"""
Легкая версия игры 2048
Двойки появляются в самых удобных для игрока местах
"""

from .base import BaseGame2048
import random


class EasyGame2048(BaseGame2048):
    """
    Легкая версия игры 2048
    Программа помогает игроку, размещая двойки в оптимальных позициях
    """

    def __init__(self):
        """Инициализация легкой версии игры"""
        super().__init__()
        self.preferred_corner = "top_left"  # Предпочитаемый угол для больших чисел

    def add_random_tile(self):
        """
        Добавляет двойку в самую удобную позицию для игрока
        Переопределяет метод базового класса
        """
        empty_cells = []
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))

        if not empty_cells:
            return

        # Случайно выбираем предпочитаемый угол в начале игры
        if len(empty_cells) > 14:  # В начале игры, когда много пустых клеток
            corners = ["top_left", "top_right", "bottom_left", "bottom_right"]
            self.preferred_corner = random.choice(corners)

        # Находим самую удобную позицию
        best_score = float("-inf")
        best_positions = []

        for i, j in empty_cells:
            score = self._evaluate_position(i, j)
            if score > best_score:
                best_score = score
                best_positions = [(i, j)]
            elif score == best_score:
                best_positions.append((i, j))

        # Если несколько позиций с одинаковой оценкой, выбираем случайную
        i, j = random.choice(best_positions)
        self.grid[i][j] = 2

    def _evaluate_position(self, i, j):
        """
        Оценивает, насколько позиция (i,j) удобна для игрока
        Возвращает числовую оценку - чем выше, тем лучше
        """
        score = 0

        # 1. Бонус за расположение в предпочитаемом углу
        if self.preferred_corner == "top_left" and i == 0 and j == 0:
            score += 100
        elif self.preferred_corner == "top_right" and i == 0 and j == 3:
            score += 100
        elif self.preferred_corner == "bottom_left" and i == 3 and j == 0:
            score += 100
        elif self.preferred_corner == "bottom_right" and i == 3 and j == 3:
            score += 100

        # 2. Бонус за расположение рядом с такими же числами (облегчает объединение)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < 4 and 0 <= nj < 4 and self.grid[ni][nj] == 2:
                score += 50  # Рядом есть такая же двойка - можно объединить

        # 3. Бонус за расположение в углах (легче создавать большие числа)
        if (i == 0 or i == 3) and (j == 0 or j == 3):
            score += 30

        # 4. Бонус за расположение рядом с большими числами (облегчает дальнейшие объединения)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < 4 and 0 <= nj < 4 and self.grid[ni][nj] > 2:
                score += self.grid[ni][nj]  # Чем больше соседнее число, тем лучше

        # 5. Бонус за расположение в направлении монотонности (помогает стратегии)
        if self.preferred_corner == "top_left":
            # Предпочтительнее левый верхний угол - поощряем позиции слева и сверху
            score += (3 - i) * 5  # Чем выше, тем лучше
            score += (3 - j) * 5  # Чем левее, тем лучше
        elif self.preferred_corner == "top_right":
            score += (3 - i) * 5  # Чем выше, тем лучше
            score += j * 5  # Чем правее, тем лучше
        elif self.preferred_corner == "bottom_left":
            score += i * 5  # Чем ниже, тем лучше
            score += (3 - j) * 5  # Чем левее, тем лучше
        elif self.preferred_corner == "bottom_right":
            score += i * 5  # Чем ниже, тем лучше
            score += j * 5  # Чем правее, тем лучше

        # 6. Штраф за создание изолированных областей
        empty_neighbors = 0
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < 4 and 0 <= nj < 4 and self.grid[ni][nj] == 0:
                empty_neighbors += 1

        if empty_neighbors == 0:
            score -= 20  # Позиция окружена - не очень хорошо

        return score
