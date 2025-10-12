"""
Базовый класс игры 2048
Содержит основную логику перемещения и объединения клеток
"""

import random


class BaseGame2048:
    """
    Базовый класс для всех версий игры 2048
    Реализует основную механику перемещения клеток и проверки окончания игры
    """

    def __init__(self):
        """Инициализация базового класса игры"""
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False

    def start_game(self):
        """
        Начало новой игры
        Сбрасывает поле, счет и добавляет две начальные двойки
        """
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """
        Добавление случайной плитки (базовая реализация)
        В случайную пустую клетку размещается двойка
        """
        empty_cells = []
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))

        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2

    def make_move(self, direction):
        """
        Выполнение хода в указанном направлении
        Возвращает True, если ход был выполнен (поле изменилось)
        """
        old_grid = [row[:] for row in self.grid]

        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        elif direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()

        # Проверяем, изменилось ли поле
        if self.grid != old_grid:
            self.add_random_tile()
            return True
        return False

    def move_left(self):
        """Перемещение всех клеток влево с объединением одинаковых"""
        for i in range(4):
            row = [self.grid[i][j] for j in range(4) if self.grid[i][j] != 0]
            new_row = []
            j = 0
            while j < len(row):
                if j < len(row) - 1 and row[j] == row[j + 1]:
                    new_row.append(row[j] * 2)
                    self.score += row[j] * 2
                    j += 2
                else:
                    new_row.append(row[j])
                    j += 1
            new_row.extend([0] * (4 - len(new_row)))
            self.grid[i] = new_row

    def move_right(self):
        """Перемещение всех клеток вправо с объединением одинаковых"""
        for i in range(4):
            row = [self.grid[i][j] for j in range(4) if self.grid[i][j] != 0]
            new_row = []
            j = len(row) - 1
            while j >= 0:
                if j > 0 and row[j] == row[j - 1]:
                    new_row.insert(0, row[j] * 2)
                    self.score += row[j] * 2
                    j -= 2
                else:
                    new_row.insert(0, row[j])
                    j -= 1
            new_row = [0] * (4 - len(new_row)) + new_row
            self.grid[i] = new_row

    def move_up(self):
        """Перемещение всех клеток вверх с объединением одинаковых"""
        for j in range(4):
            col = [self.grid[i][j] for i in range(4) if self.grid[i][j] != 0]
            new_col = []
            i = 0
            while i < len(col):
                if i < len(col) - 1 and col[i] == col[i + 1]:
                    new_col.append(col[i] * 2)
                    self.score += col[i] * 2
                    i += 2
                else:
                    new_col.append(col[i])
                    i += 1
            new_col.extend([0] * (4 - len(new_col)))
            for i in range(4):
                self.grid[i][j] = new_col[i]

    def move_down(self):
        """Перемещение всех клеток вниз с объединением одинаковых"""
        for j in range(4):
            col = [self.grid[i][j] for i in range(4) if self.grid[i][j] != 0]
            new_col = []
            i = len(col) - 1
            while i >= 0:
                if i > 0 and col[i] == col[i - 1]:
                    new_col.insert(0, col[i] * 2)
                    self.score += col[i] * 2
                    i -= 2
                else:
                    new_col.insert(0, col[i])
                    i -= 1
            new_col = [0] * (4 - len(new_col)) + new_col
            for i in range(4):
                self.grid[i][j] = new_col[i]

    def is_game_over(self):
        """
        Проверка окончания игры
        Возвращает True, если нет возможных ходов
        """
        # Проверяем, есть ли пустые клетки
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False

        # Проверяем, есть ли возможные объединения
        for i in range(4):
            for j in range(4):
                current = self.grid[i][j]
                if j < 3 and self.grid[i][j + 1] == current:
                    return False
                if i < 3 and self.grid[i + 1][j] == current:
                    return False

        return True
