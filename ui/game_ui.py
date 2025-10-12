"""
Пользовательский интерфейс для обычных версий игры 2048
Наследует базовый UI и добавляет обработку игровой логики
"""

import tkinter as tk
from .base_ui import Base2048UI


class Game2048UI(Base2048UI):
    """
    UI для обычных версий игры 2048
    Связывает интерфейс с игровой логикой и обрабатывает пользовательский ввод
    """

    def __init__(self, game_logic, title="2048"):
        """
        Инициализация игрового UI
        game_logic - объект игровой логики (из core)
        title - заголовок окна
        """
        super().__init__(title)
        self.game_logic = game_logic
        self.setup_ui()

        # Привязка обработчиков клавиш
        self.window.bind("<Key>", self.key_handler)

    def setup_ui(self):
        """Настройка интерфейса - создает все элементы управления"""
        main_frame = tk.Frame(self.window, padx=10, pady=10, bg="#FAF8EF")
        main_frame.pack()

        # Заголовок и счет
        self.create_header(main_frame)

        # Игровое поле
        self.create_grid(main_frame)

        # Панель управления
        move_handlers = {
            "up": lambda: self.move("up"),
            "down": lambda: self.move("down"),
            "left": lambda: self.move("left"),
            "right": lambda: self.move("right"),
        }
        self.create_controls(main_frame, move_handlers)

        # Кнопка новой игры
        self.create_new_game_button(main_frame, self.start_game)

        self.update_display()

    def start_game(self):
        """Начало новой игры - сброс состояния и обновление отображения"""
        self.game_logic.start_game()
        self.update_display()

    def move(self, direction):
        """
        Обработка хода в указанном направлении
        direction - одно из: 'up', 'down', 'left', 'right'
        """
        if self.game_logic.game_over:
            return

        moved = self.game_logic.make_move(direction)
        if moved:
            self.update_display()

            if self.game_logic.is_game_over():
                self.game_logic.game_over = True
                self.show_game_over(self.game_logic.score)

    def key_handler(self, event):
        """
        Обработка нажатий клавиш
        Поддерживает WASD, ЦФЫВ и стрелки для управления
        """
        char = event.char.lower()
        key = event.keysym.lower()

        if key in ["up", "w"] or char in ["ц", "w"]:
            self.move("up")
        elif key in ["down", "s"] or char in ["ы", "s"]:
            self.move("down")
        elif key in ["left", "a"] or char in ["ф", "a"]:
            self.move("left")
        elif key in ["right", "d"] or char in ["в", "d"]:
            self.move("right")

    def update_display(self):
        """Полное обновление отображения - сетка и счет"""
        self.update_grid_display(self.game_logic.grid)
        self.update_score(self.game_logic.score)
