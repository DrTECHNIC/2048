"""
Базовый класс пользовательского интерфейса для тренажеров 2048
Содержит специализированные элементы для solver'ов с подсказками и предпросмотром
"""

import tkinter as tk
from .base_ui import Base2048UI


class Solver2048UI(Base2048UI):
    """
    Базовый класс для UI тренажеров 2048
    Расширяет базовый UI элементами для отображения подсказок и рекомендуемых ходов
    """

    def __init__(self, title="2048 Solver"):
        """
        Инициализация UI тренажера
        Создает дополнительные элементы для отображения рекомендуемых ходов
        """
        super().__init__(title)

    def create_direction_display(self, parent, initial_text=""):
        """
        Создание метки для отображения рекомендуемого направления хода
        Возвращает созданный виджет метки
        """
        direction_label = tk.Label(
            parent,
            text=initial_text,
            font=("Arial", 14, "bold"),
            height=2,
            bg="#FAF8EF",
            fg="#776E65",
        )
        direction_label.pack(pady=10)
        return direction_label

    def create_preview_grid(self, parent, title="Предпросмотр"):
        """
        Создание дополнительного игрового поля для предпросмотра хода
        Возвращает список клеток для отображения состояния после хода
        """
        # Заголовок предпросмотра
        preview_label = tk.Label(
            parent, text=title, font=("Arial", 12, "bold"), bg="#FAF8EF", fg="#776E65"
        )
        preview_label.pack()

        # Фрейм для сетки предпросмотра
        preview_frame = tk.Frame(parent, bg="#BBADA0", padx=5, pady=5)
        preview_frame.pack(pady=5)

        preview_cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(preview_frame, width=60, height=60, bg="#CDC1B4")
                cell.grid(row=i, column=j, padx=3, pady=3)
                cell.pack_propagate(False)

                label = tk.Label(
                    cell,
                    text="",
                    font=("Arial", 16, "bold"),
                    justify="center",
                    bg="#CDC1B4",
                    fg="#776E65",
                )
                label.pack(expand=True, fill="both")
                row.append(label)
            preview_cells.append(row)

        return preview_cells

    def update_preview_grid(self, preview_cells, grid):
        """
        Обновление сетки предпросмотра на основе переданного состояния
        preview_cells - список клеток предпросмотра
        grid - двумерный список с состоянием для отображения
        """
        for i in range(4):
            for j in range(4):
                value = grid[i][j]
                bg_color, frame_color, text_color = self.COLORS.get(
                    value, ("#3C3A32", "#3C3A32", "#F9F6F2")
                )

                preview_cells[i][j].config(
                    text=str(value) if value != 0 else "", bg=bg_color, fg=text_color
                )
                preview_cells[i][j].master.config(bg=frame_color)

    def create_control_buttons(self, parent, button_configs):
        """
        Создание набора кнопок управления для тренажера
        button_configs - список кортежей (текст, обработчик, состояние)
        """
        button_frame = tk.Frame(parent, bg="#FAF8EF")
        button_frame.pack(pady=10)

        buttons = {}
        for i, (text, command, state) in enumerate(button_configs):
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 10),
                command=command,
                bg="#8F7A66",
                fg="#F9F6F2",
                relief="raised",
                bd=2,
                state=state,
            )
            btn.grid(row=0, column=i, padx=5)
            buttons[text] = btn

        return buttons

    def update_direction_display(self, direction_label, direction):
        """
        Обновление отображения рекомендуемого направления хода
        direction_label - виджет метки для отображения
        direction - строка с направлением ('up', 'down', 'left', 'right')
        """
        direction_texts = {
            "up": "Рекомендуемый ход: ВВЕРХ",
            "down": "Рекомендуемый ход: ВНИЗ",
            "left": "Рекомендуемый ход: ВЛЕВО",
            "right": "Рекомендуемый ход: ВПРАВО",
            "": "Разместите двойки на поле",
        }

        text = direction_texts.get(direction, direction)
        direction_label.config(text=text)
