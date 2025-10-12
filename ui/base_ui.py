"""
Базовый класс пользовательского интерфейса для всех версий 2048
Содержит общие элементы интерфейса и методы отображения
"""

import tkinter as tk
from tkinter import messagebox


class Base2048UI:
    """
    Базовый класс для UI всех версий 2048
    Реализует общие элементы: игровое поле, счет, кнопки управления
    Использует оригинальную цветовую схему игры 2048
    """

    # Цветовая схема (оригинальная палитра 2048)
    COLORS = {
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

    def __init__(self, title="2048"):
        """
        Инициализация базового UI
        Создает главное окно с указанным заголовком
        """
        self.window = tk.Tk()
        self.window.title(title)
        self.window.resizable(False, False)
        self.window.configure(bg="#FAF8EF")

    def create_header(self, parent):
        """
        Создание заголовка и счета
        Возвращает фрейм с элементами заголовка
        """
        header_frame = tk.Frame(parent, bg="#FAF8EF")
        header_frame.pack(pady=10)

        # Заголовок
        title_label = tk.Label(
            header_frame,
            text="2048",
            font=("Arial", 24, "bold"),
            bg="#FAF8EF",
            fg="#776E65",
        )
        title_label.pack(side=tk.LEFT, padx=20)

        # Счет
        score_frame = tk.Frame(header_frame, bg="#FAF8EF")
        score_frame.pack(side=tk.RIGHT, padx=20)

        tk.Label(
            score_frame, text="Счет:", font=("Arial", 12), bg="#FAF8EF", fg="#776E65"
        ).pack()

        self.score_label = tk.Label(
            score_frame,
            text="0",
            font=("Arial", 16, "bold"),
            bg="#FAF8EF",
            fg="#776E65",
        )
        self.score_label.pack()

        return header_frame

    def create_grid(self, parent, click_handler=None):
        """
        Создание игрового поля 4x4
        Если передан click_handler, клетки становятся кликабельными
        """
        grid_frame = tk.Frame(parent, bg="#BBADA0", padx=5, pady=5)
        grid_frame.pack(pady=10)

        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(grid_frame, width=80, height=80, bg="#CDC1B4")
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

                # Привязка обработчика клика, если передан
                if click_handler:
                    label.bind(
                        "<Button-1>", lambda e, row=i, col=j: click_handler(row, col)
                    )
                    cell.bind(
                        "<Button-1>", lambda e, row=i, col=j: click_handler(row, col)
                    )

                row.append(label)
            self.cells.append(row)

        return grid_frame

    def create_controls(self, parent, move_handlers):
        """
        Создание панели управления с кнопками направлений
        move_handlers - словарь с функциями для каждого направления
        """
        control_frame = tk.Frame(parent, bg="#FAF8EF")
        control_frame.pack(pady=10)

        # Кнопки управления
        buttons_config = [
            ("↑", 0, 1, "up"),
            ("←", 1, 0, "left"),
            ("↓", 1, 1, "down"),
            ("→", 1, 2, "right"),
        ]

        for text, row, col, direction in buttons_config:
            btn = tk.Button(
                control_frame,
                text=text,
                font=("Arial", 16, "bold"),
                width=3,
                height=1,
                command=move_handlers[direction],
                bg="#8F7A66",
                fg="#F9F6F2",
                relief="raised",
                bd=3,
            )
            btn.grid(row=row, column=col, padx=5, pady=2)

        return control_frame

    def create_new_game_button(self, parent, handler):
        """
        Создание кнопки новой игры
        handler - функция, вызываемая при нажатии кнопки
        """
        btn = tk.Button(
            parent,
            text="Новая игра",
            font=("Arial", 12),
            command=handler,
            bg="#8F7A66",
            fg="#F9F6F2",
            relief="raised",
            bd=2,
        )
        btn.pack(pady=5)
        return btn

    def update_grid_display(self, grid):
        """
        Обновление отображения сетки на основе переданного состояния
        grid - двумерный список с состоянием игрового поля
        """
        for i in range(4):
            for j in range(4):
                value = grid[i][j]
                bg_color, frame_color, text_color = self.COLORS.get(
                    value, ("#3C3A32", "#3C3A32", "#F9F6F2")
                )

                self.cells[i][j].config(
                    text=str(value) if value != 0 else "", bg=bg_color, fg=text_color
                )
                self.cells[i][j].master.config(bg=frame_color)

    def update_score(self, score):
        """Обновление отображения счета"""
        self.score_label.config(text=str(score))

    def show_game_over(self, score):
        """Показать сообщение об окончании игры"""
        messagebox.showinfo("Игра окончена", f"Игра окончена! Ваш счет: {score}")

    def run(self):
        """Запуск главного цикла приложения"""
        self.window.mainloop()
