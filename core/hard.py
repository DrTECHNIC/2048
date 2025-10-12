"""
Сложная версия игры 2048
Двойки появляются в самых неудобных для игрока местах
"""

from .base import BaseGame2048
import random


class HardGame2048(BaseGame2048):
    """
    Сложная версия игры 2048
    Программа противодействует игроку, размещая двойки в худших позициях
    """

    def __init__(self):
        """Инициализация сложной версии игры"""
        super().__init__()

    def add_random_tile(self):
        """
        Добавляет двойку в самую неудобную позицию для игрока
        Переопределяет метод базового класса
        """
        empty_cells = []
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))

        if not empty_cells:
            return

        # Находим самую неудобную позицию
        worst_score = float("-inf")
        worst_positions = []

        for i, j in empty_cells:
            score = self._evaluate_position(i, j)
            if score > worst_score:
                worst_score = score
                worst_positions = [(i, j)]
            elif score == worst_score:
                worst_positions.append((i, j))

        # Если несколько позиций с одинаковой оценкой, выбираем случайную
        i, j = random.choice(worst_positions)
        self.grid[i][j] = 2

    def _evaluate_position(self, i, j):
        """
        Оценивает, насколько позиция (i,j) неудобна для игрока
        Возвращает числовую оценку - чем выше, тем хуже для игрока
        """
        score = 0

        # 1. Штраф за расположение рядом с большими числами (мешает объединению)
        neighbors = 0
        neighbor_sum = 0
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < 4 and 0 <= nj < 4 and self.grid[ni][nj] != 0:
                neighbors += 1
                neighbor_sum += self.grid[ni][nj]

        if neighbors > 0:
            # Чем больше соседи и чем больше их значения, тем хуже позиция
            score += neighbors * 10
            score += neighbor_sum

        # 2. Штраф за создание изолированных областей
        for dx, dy in [(0, 1), (1, 0)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < 4 and 0 <= nj < 4 and self.grid[ni][nj] == 2:
                # Если есть возможность объединения, это плохо для компьютера
                score -= 50

        # 3. Поощрение расположения в углах (сложнее управлять большими числами)
        if (i == 0 or i == 3) and (j == 0 or j == 3):
            score += 30

        # 4. Поощрение расположения в центре (усложняет маневрирование)
        if 1 <= i <= 2 and 1 <= j <= 2:
            score += 20

        # 5. Штраф за расположение в ряду/колонке с возможными объединениями
        for x in range(4):
            if x != j and self.grid[i][x] == 2:
                score -= 20  # Есть потенциальное объединение в строке
            if x != i and self.grid[x][j] == 2:
                score -= 20  # Есть потенциальное объединение в столбце

        return score
