"""
Быстрый тренажер для игры 2048 с автоматическим применением ходов
После размещения двойки сразу применяет лучший ход и обновляет поле
Предназначен для быстрого изучения стратегий без ручного подтверждения
"""

import tkinter as tk
import sys
import os

# Добавляем путь для импорта модулей из корневой директории
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from solvers.base import SolverBase2048  # noqa: E402


class PracticeFastGame(SolverBase2048):
    """
    Класс игровой логики для быстрого тренажера
    Автоматически применяет лучший ход после размещения двойки пользователем
    Упрощает процесс обучения за счет автоматизации рутинных действий
    """

    def __init__(self):
        """Инициализация быстрого тренажера"""
        super().__init__()
        self.placed_tiles = 0
        self.is_first_move = True
        self.best_move_direction = ""

    def start_game(self):
        """Начало новой игры - сброс состояния, счета и счетчиков"""
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.placed_tiles = 0
        self.is_first_move = True
        self.best_move_direction = ""

    def place_tile(self, i, j):
        """
        Размещение двойки на поле и автоматическое применение лучшего хода
        Возвращает True, если размещение прошло успешно
        """
        if self.grid[i][j] != 0:
            return False

        self.grid[i][j] = 2
        self.placed_tiles += 1

        # Проверка условий для расчета хода
        if self.is_first_move and self.placed_tiles == 2:
            self.calculate_and_apply_best_move()
            self.is_first_move = False
            self.placed_tiles = 0
        elif not self.is_first_move and self.placed_tiles == 1:
            self.calculate_and_apply_best_move()
            self.placed_tiles = 0

        return True

    def calculate_and_apply_best_move(self):
        """Вычисление и применение лучшего хода для текущего состояния"""
        best_move, best_state, _ = self.calculate_best_move(self.grid)

        if best_move:
            self.grid = best_state
            self.best_move_direction = best_move
        else:
            self.best_move_direction = "Нет возможных ходов"


class PracticeFastUI:
    """
    Пользовательский интерфейс для быстрого тренажера 2048
    Предоставляет упрощенный интерфейс с автоматическим применением ходов
    Идеален для быстрого ознакомления с основными стратегиями игры
    """

    def __init__(self):
        """Инициализация UI быстрого тренажера"""
        self.window = tk.Tk()
        self.window.title("2048 Practice - Fast")
        self.window.resizable(False, False)

        self.game_logic = PracticeFastGame()
        self.setup_ui()

    def setup_ui(self):
        """Настройка пользовательского интерфейса с одним игровым полем"""
        # Основной фрейм
        main_frame = tk.Frame(self.window, padx=10, pady=10)
        main_frame.pack()

        # Заголовок
        tk.Label(
            main_frame, text="2048 Practice - Fast", font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Игровое поле
        self.grid_frame = tk.Frame(main_frame, bg="#BBADA0", padx=5, pady=5)
        self.grid_frame.pack(pady=10)

        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(self.grid_frame, width=80, height=80, bg="#CDC1B4")
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
            self.cells.append(row)

        # Метка с направлением хода
        self.direction_label = tk.Label(
            main_frame,
            text="Разместите две двойки на поле",
            font=("Arial", 14, "bold"),
            height=2,
        )
        self.direction_label.pack(pady=10)

        # Кнопка сброса
        reset_btn = tk.Button(
            main_frame, text="Новая игра", command=self.reset_game, font=("Arial", 12)
        )
        reset_btn.pack(pady=5)

        # Привязка кликов к клеткам
        for i in range(4):
            for j in range(4):
                self.cells[i][j].bind(
                    "<Button-1>", lambda event, row=i, col=j: self.place_tile(row, col)
                )

        self.update_display()

    def place_tile(self, i, j):
        """Обработка клика по клетке для размещения двойки"""
        if self.game_logic.place_tile(i, j):
            self.update_display()

            # Обновление направления хода
            direction_text = {
                "up": "Ход: ВВЕРХ",
                "down": "Ход: ВНИЗ",
                "left": "Ход: ВЛЕВО",
                "right": "Ход: ВПРАВО",
            }

            text = direction_text.get(
                self.game_logic.best_move_direction,
                self.game_logic.best_move_direction,
            )
            self.direction_label.config(text=text)

    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        self.game_logic.start_game()
        self.direction_label.config(text="Разместите две двойки на поле")
        self.update_display()

    def update_display(self):
        """Обновление отображения игрового поля"""
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

        # Обновление игрового поля
        for i in range(4):
            for j in range(4):
                value = self.game_logic.grid[i][j]
                bg_color, frame_color, text_color = colors.get(
                    value, ("#3C3A32", "#3C3A32", "#F9F6F2")
                )

                self.cells[i][j].config(
                    text=str(value) if value != 0 else "", bg=bg_color, fg=text_color
                )
                self.cells[i][j].master.config(bg=frame_color)

    def run(self):
        """Запуск главного цикла приложения"""
        self.window.mainloop()


if __name__ == "__main__":
    app = PracticeFastUI()
    app.run()
