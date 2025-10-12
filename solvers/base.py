"""
Базовый класс для решателей игры 2048
Содержит общую логику оценки состояния и симуляции ходов
"""

import copy


class SolverBase2048:
    """
    Базовый класс для всех решателей 2048
    Предоставляет методы для симуляции ходов и оценки игровых состояний
    Может быть унаследован для создания различных стратегий решения
    """

    def __init__(self):
        """Инициализация базового решателя"""
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False

    def simulate_move(self, grid, direction):
        """
        Симуляция хода в указанном направлении без изменения основного состояния
        Возвращает новое состояние игрового поля после выполнения хода
        """
        new_grid = copy.deepcopy(grid)

        if direction == "left":
            for i in range(4):
                row = [new_grid[i][j] for j in range(4) if new_grid[i][j] != 0]
                j = 0
                while j < len(row) - 1:
                    if row[j] == row[j + 1]:
                        row[j] *= 2
                        row.pop(j + 1)
                    j += 1
                row.extend([0] * (4 - len(row)))
                new_grid[i] = row

        elif direction == "right":
            for i in range(4):
                row = [new_grid[i][j] for j in range(4) if new_grid[i][j] != 0]
                j = len(row) - 1
                while j > 0:
                    if row[j] == row[j - 1]:
                        row[j] *= 2
                        row.pop(j - 1)
                        j -= 1
                    j -= 1
                new_grid[i] = [0] * (4 - len(row)) + row

        elif direction == "up":
            for j in range(4):
                col = [new_grid[i][j] for i in range(4) if new_grid[i][j] != 0]
                i = 0
                while i < len(col) - 1:
                    if col[i] == col[i + 1]:
                        col[i] *= 2
                        col.pop(i + 1)
                    i += 1
                col.extend([0] * (4 - len(col)))
                for i in range(4):
                    new_grid[i][j] = col[i]

        elif direction == "down":
            for j in range(4):
                col = [new_grid[i][j] for i in range(4) if new_grid[i][j] != 0]
                i = len(col) - 1
                while i > 0:
                    if col[i] == col[i - 1]:
                        col[i] *= 2
                        col.pop(i - 1)
                        i -= 1
                    i -= 1
                for i in range(4):
                    new_grid[i][j] = 0
                for i in range(len(col)):
                    new_grid[4 - len(col) + i][j] = col[i]

        return new_grid

    def evaluate_state(self, grid):
        """
        Оценка состояния игрового поля с использованием эвристик
        Возвращает числовую оценку - чем выше, тем лучше состояние для игрока
        """
        score = 0
        empty_cells = 0
        max_tile = 0

        # Предпочтение пустым клеткам (больше возможностей для маневра)
        for i in range(4):
            for j in range(4):
                if grid[i][j] == 0:
                    empty_cells += 1
                else:
                    if grid[i][j] > max_tile:
                        max_tile = grid[i][j]

                    # Предпочтение большим числам в углах (стратегия угла)
                    if (i == 0 or i == 3) and (j == 0 or j == 3):
                        score += grid[i][j] * 10
                    else:
                        score += grid[i][j]

        # Монотонность - предпочтение упорядоченным строкам/столбцам
        monotonicity = self.calculate_monotonicity(grid)

        score += empty_cells * 100
        score += max_tile * 20
        score += monotonicity * 5

        return score

    def calculate_monotonicity(self, grid):
        """
        Вычисление монотонности строк и столбцов
        Возвращает оценку монотонности - чем выше, тем более упорядочено поле
        """
        monotonicity = 0

        # Проверка строк на монотонность (слева направо и справа налево)
        for i in range(4):
            for j in range(3):
                if grid[i][j] >= grid[i][j + 1]:
                    monotonicity += 1
                if grid[i][3 - j] >= grid[i][2 - j]:
                    monotonicity += 1

        # Проверка столбцов на монотонность (сверху вниз и снизу вверх)
        for j in range(4):
            for i in range(3):
                if grid[i][j] >= grid[i + 1][j]:
                    monotonicity += 1
                if grid[3 - i][j] >= grid[2 - i][j]:
                    monotonicity += 1

        return monotonicity

    def calculate_best_move(self, grid):
        """
        Вычисление лучшего хода для данного состояния поля
        Возвращает кортеж (направление, новое_состояние, оценка)
        """
        best_score = -1
        best_move = None
        best_state = None

        # Проверка всех возможных ходов
        for direction in ["up", "down", "left", "right"]:
            new_state = self.simulate_move(copy.deepcopy(grid), direction)
            if new_state != grid:  # Ход возможен только если состояние изменилось
                score = self.evaluate_state(new_state)
                if score > best_score:
                    best_score = score
                    best_move = direction
                    best_state = new_state

        return best_move, best_state, best_score
