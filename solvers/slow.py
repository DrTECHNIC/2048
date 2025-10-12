"""
Медленный тренажер для игры 2048 с подсказками и подтверждением ходов
Позволяет пользователю размещать двойки и видеть рекомендуемые ходы с предпросмотром
"""

import tkinter as tk
import sys
import os

# Добавляем путь для импорта модулей из корневой директории
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from solvers.base import SolverBase2048  # noqa: E402


class PracticeSlowGame(SolverBase2048):
    """
    Класс игровой логики для медленного тренажера
    Наследует базовый решатель и добавляет управление размещением двоек и отменой
    Позволяет пользователю изучать стратегию шаг за шагом
    """

    def __init__(self):
        """Инициализация медленного тренажера"""
        super().__init__()
        self.placed_tiles = []
        self.is_first_move = True
        self.best_move_state = None
        self.best_move_direction = ""

    def start_game(self):
        """Начало новой игры - сброс состояния, счета и всех флагов"""
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.placed_tiles = []
        self.is_first_move = True
        self.best_move_state = None
        self.best_move_direction = ""

    def place_tile(self, i, j):
        """
        Размещение двойки на поле в указанной позиции
        Возвращает True, если размещение прошло успешно
        """
        if self.grid[i][j] != 0:
            return False

        # Определяем максимальное количество ячеек для текущего хода
        max_tiles = 2 if self.is_first_move else 1

        # Если достигнут лимит, удаляем самую старую ячейку
        if len(self.placed_tiles) >= max_tiles:
            old_i, old_j = self.placed_tiles.pop(0)
            self.grid[old_i][old_j] = 0

        # Размещаем новую двойку
        self.grid[i][j] = 2
        self.placed_tiles.append((i, j))

        # Проверка условий для расчета хода
        if self.is_first_move and len(self.placed_tiles) == 2:
            self.calculate_best_move_internal()
        elif not self.is_first_move and len(self.placed_tiles) == 1:
            self.calculate_best_move_internal()

        return True

    def undo_placement(self):
        """Отмена последнего размещения двойки"""
        if not self.placed_tiles:
            return

        # Удаление последней размещенной двойки
        i, j = self.placed_tiles.pop()
        self.grid[i][j] = 0

        # Сброс расчета хода
        self.best_move_state = None
        self.best_move_direction = ""

    def calculate_best_move_internal(self):
        """Внутренний расчет лучшего хода для текущего состояния поля"""
        best_move, best_state, _ = self.calculate_best_move(self.grid)

        if best_move:
            self.best_move_direction = best_move
            self.best_move_state = best_state
        else:
            self.best_move_direction = "Нет возможных ходов"
            self.best_move_state = None

    def apply_best_move(self):
        """
        Применение лучшего хода к текущему состоянию
        Возвращает True, если ход был успешно применен
        """
        if self.best_move_state is not None:
            self.grid = self.best_move_state
            self.placed_tiles.clear()
            self.is_first_move = False
            self.best_move_state = None
            self.best_move_direction = ""
            return True
        return False


class PracticeSlowUI:
    """
    Пользовательский интерфейс для медленного тренажера 2048
    Обеспечивает отображение текущего состояния, предпросмотр хода и управление
    Предназначен для детального изучения стратегий игры
    """

    def __init__(self):
        """Инициализация UI медленного тренажера"""
        self.window = tk.Tk()
        self.window.title("2048 Practice - Slow")
        self.window.resizable(False, False)

        self.game_logic = PracticeSlowGame()
        self.setup_ui()

    def setup_ui(self):
        """Настройка пользовательского интерфейса с двумя игровыми полями"""
        # Основной фрейм
        main_frame = tk.Frame(self.window, padx=10, pady=10)
        main_frame.pack()

        # Фрейм для полей игры
        fields_frame = tk.Frame(main_frame)
        fields_frame.pack(pady=10)

        # Левое поле - текущая игра
        left_frame = tk.Frame(fields_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(left_frame, text="Текущая игра", font=("Arial", 12, "bold")).pack()

        self.left_grid_frame = tk.Frame(left_frame, bg="#BBADA0", padx=5, pady=5)
        self.left_grid_frame.pack(pady=5)

        self.left_cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(self.left_grid_frame, width=80, height=80, bg="#CDC1B4")
                cell.grid(row=i, column=j, padx=5, pady=5)
                cell.pack_propagate(False)

                label = tk.Label(
                    cell,
                    text="",
                    font=("Arial", 20, "bold"),
                    justify="center",
                    bg="#CDC1B4",
                    fg="#776E65",
                )
                label.pack(expand=True, fill="both")
                row.append(label)
            self.left_cells.append(row)

        # Кнопка отменить под левым полем
        self.undo_btn = tk.Button(
            left_frame,
            text="Отменить",
            command=self.undo_placement,
            state=tk.DISABLED,
            font=("Arial", 12),
        )
        self.undo_btn.pack(pady=5)

        # Правое поле - лучший ход
        right_frame = tk.Frame(fields_frame)
        right_frame.pack(side=tk.RIGHT, padx=10)

        # Метка с направлением хода
        self.direction_label = tk.Label(
            right_frame, text="", font=("Arial", 14, "bold"), height=2
        )
        self.direction_label.pack()

        tk.Label(
            right_frame, text="После лучшего хода", font=("Arial", 12, "bold")
        ).pack()

        self.right_grid_frame = tk.Frame(right_frame, bg="#BBADA0", padx=5, pady=5)
        self.right_grid_frame.pack(pady=5)

        self.right_cells = []
        for i in range(4):
            row = []
            for j in range(4):
                label = tk.Label(
                    self.right_grid_frame,
                    width=10,
                    height=4,
                    text="",
                    font=("Arial", 20, "bold"),
                    justify="center",
                    relief="solid",
                    borderwidth=1,
                    bg="#CDC1B4",
                    fg="#776E65",
                )
                label.grid(row=i, column=j, padx=5, pady=5)
                row.append(label)
            self.right_cells.append(row)

        # Кнопка применить под правым полем
        self.apply_btn = tk.Button(
            right_frame,
            text="Применить",
            command=self.apply_best_move,
            state=tk.DISABLED,
            font=("Arial", 12),
        )
        self.apply_btn.pack(pady=5)

        # Привязка кликов к клеткам левого поля
        for i in range(4):
            for j in range(4):
                self.left_cells[i][j].bind(
                    "<Button-1>", lambda event, row=i, col=j: self.place_tile(row, col)
                )

        self.update_display()

    def place_tile(self, i, j):
        """Обработка клика по клетке для размещения двойки"""
        if self.game_logic.place_tile(i, j):
            self.undo_btn.config(state=tk.NORMAL)
            self.update_display()

            if self.game_logic.best_move_state is not None:
                self.apply_btn.config(state=tk.NORMAL)

    def undo_placement(self):
        """Обработка отмены размещения двойки"""
        self.game_logic.undo_placement()

        if not self.game_logic.placed_tiles:
            self.undo_btn.config(state=tk.DISABLED)
            self.apply_btn.config(state=tk.DISABLED)

        self.update_display()

    def apply_best_move(self):
        """Применение лучшего хода и обновление состояния"""
        if self.game_logic.apply_best_move():
            self.undo_btn.config(state=tk.DISABLED)
            self.apply_btn.config(state=tk.DISABLED)
            self.update_display()

    def update_display(self):
        """Обновление отображения обоих игровых полей"""
        colors = {
            0: ("#CDC1B4", "#CDC1B4", "#776E65"),
            2: ("#EEE4DA", "#EEE4DA", "#776E65"),
            4: ("#EDE0C8", "#EDE0C8", "#776E65"),
            8: ("#F2B179", "#F2B179", "#F9F6F2"),
            16: ("#F59563", "#F59563", "#F9F6F2"),
            32: ("#F67C5F", "#F67C5F", "#F9F6F2"),
            64: ("#F65E3B", "#F65E3B", "#F9F6F2"),
            128: ("#EDCF72", "#EDCF72", "#F9F6F2"),
            256: ("#EDCC61", "#EDCC61", "#F9F6F2"),
            512: ("#EDC850", "#EDC850", "#F9F6F2"),
            1024: ("#EDC53F", "#EDC53F", "#F9F6F2"),
            2048: ("#EDC22E", "#EDC22E", "#F9F6F2"),
            4096: ("#3C3A32", "#3C3A32", "#F9F6F2"),
            8192: ("#3C3A32", "#3C3A32", "#F9F6F2"),
        }

        # Обновление левого поля (текущее состояние)
        for i in range(4):
            for j in range(4):
                value = self.game_logic.grid[i][j]
                bg_color, frame_color, text_color = colors.get(
                    value, ("#3C3A32", "#3C3A32", "#F9F6F2")
                )

                self.left_cells[i][j].config(
                    text=str(value) if value != 0 else "", bg=bg_color, fg=text_color
                )
                self.left_cells[i][j].master.config(bg=frame_color)

        # Обновление правого поля и направления
        direction_text = {
            "up": "Ход: ВВЕРХ",
            "down": "Ход: ВНИЗ",
            "left": "Ход: ВЛЕВО",
            "right": "Ход: ВПРАВО",
        }

        self.direction_label.config(
            text=direction_text.get(
                self.game_logic.best_move_direction,
                self.game_logic.best_move_direction,
            )
        )

        if self.game_logic.best_move_state:
            for i in range(4):
                for j in range(4):
                    value = self.game_logic.best_move_state[i][j]
                    bg_color, frame_color, text_color = colors.get(
                        value, ("#3C3A32", "#3C3A32", "#F9F6F2")
                    )

                    self.right_cells[i][j].config(
                        text=str(value) if value != 0 else "",
                        bg=bg_color,
                        fg=text_color,
                    )
        else:
            for i in range(4):
                for j in range(4):
                    self.right_cells[i][j].config(text="", bg="#CDC1B4")

    def run(self):
        """Запуск главного цикла приложения"""
        self.window.mainloop()


if __name__ == "__main__":
    app = PracticeSlowUI()
    app.run()
