"""
Главный хаб для выбора и запуска различных версий 2048
Предоставляет единую точку входа во все варианты игры через удобное меню
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Добавляем пути для импорта модулей проекта
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core.normal import NormalGame2048  # noqa: E402
from core.easy import EasyGame2048  # noqa: E402
from core.hard import HardGame2048  # noqa: E402
from solvers.slow import PracticeSlowUI  # noqa: E402
from solvers.fast import PracticeFastUI  # noqa: E402
from ui.game_ui import Game2048UI  # noqa: E402


class MainHub:
    """
    Главный хаб для выбора и запуска версий 2048
    Предоставляет интерфейс для выбора между обычными играми и тренажерами
    Обеспечивает удобную навигацию между различными режимами игры
    """

    def __init__(self):
        """
        Инициализация главного хаба
        Создает главное окно и настраивает пользовательский интерфейс
        """
        self.window = tk.Tk()
        self.window.title("2048 Game Hub")
        self.window.geometry("450x650")
        self.window.resizable(False, False)
        self.window.configure(bg="#FAF8EF")

        self.setup_ui()

    def setup_ui(self):
        """Настройка пользовательского интерфейса хаба"""
        # Основной фрейм
        main_frame = tk.Frame(self.window, padx=20, pady=20, bg="#FAF8EF")
        main_frame.pack(expand=True, fill="both")

        # Заголовок
        title_label = tk.Label(
            main_frame,
            text="2048 Game Collection",
            font=("Arial", 24, "bold"),
            bg="#FAF8EF",
            fg="#776E65",
        )
        title_label.pack(pady=20)

        # Описание
        desc_label = tk.Label(
            main_frame,
            text="Выберите версию игры:",
            font=("Arial", 12),
            bg="#FAF8EF",
            fg="#666666",
        )
        desc_label.pack(pady=10)

        # Кнопки выбора версий
        versions = [
            ("🎮 Обычная версия", self.run_normal),
            ("😊 Легкая версия", self.run_easy),
            ("😈 Сложная версия", self.run_hard),
            ("🎯 Тренажер (медленный)", self.run_practice_slow),
            ("⚡ Тренажер (быстрый)", self.run_practice_fast),
        ]

        for text, command in versions:
            btn = tk.Button(
                main_frame,
                text=text,
                font=("Arial", 12),
                command=command,
                bg="#8F7A66",
                fg="#F9F6F2",
                relief="raised",
                bd=3,
                width=20,
                height=2,
            )
            btn.pack(pady=8)

        # Инструкция по управлению
        instruction_frame = tk.Frame(main_frame, bg="#FAF8EF")
        instruction_frame.pack(pady=15)

        instruction_label = tk.Label(
            instruction_frame,
            text="🎮 Управление в играх:",
            font=("Arial", 11, "bold"),
            bg="#FAF8EF",
            fg="#776E65",
        )
        instruction_label.pack()

        controls_text = (
            "• Стрелки: Вверх, Вниз, Влево, Вправо\n"
            "• WASD: W-Вверх, A-Влево, S-Вниз, D-Вправо\n"
            "• ЦФЫВ: Ц-Вверх, Ф-Влево, Ы-Вниз, В-Вправо"
        )

        controls_label = tk.Label(
            instruction_frame,
            text=controls_text,
            font=("Arial", 9),
            bg="#FAF8EF",
            fg="#666666",
            justify="left",
        )
        controls_label.pack(pady=5)

        # Разделитель перед инструкцией
        separator1 = ttk.Separator(main_frame, orient="horizontal")
        separator1.pack(fill="x", pady=20)

        # Инструкция по управлению - более заметная
        instruction_frame = tk.Frame(
            main_frame, bg="#EDE0C8", relief="solid", bd=1, padx=15, pady=10
        )
        instruction_frame.pack(pady=10, fill="x")

        instruction_title = tk.Label(
            instruction_frame,
            text="🎮 Управление в играх",
            font=("Arial", 13, "bold"),
            bg="#EDE0C8",
            fg="#776E65",
        )
        instruction_title.pack(pady=(0, 8))

        # Создаем фрейм для колонок с управлениями
        controls_frame = tk.Frame(instruction_frame, bg="#EDE0C8")
        controls_frame.pack(fill="x")

        # Левая колонка - стрелки
        left_column = tk.Frame(controls_frame, bg="#EDE0C8")
        left_column.pack(side="left", expand=True)

        arrow_label = tk.Label(
            left_column,
            text="Стрелки:",
            font=("Arial", 10, "bold"),
            bg="#EDE0C8",
            fg="#776E65",
        )
        arrow_label.pack(anchor="w")

        arrow_keys = tk.Label(
            left_column,
            text="↑ Вверх\n↓ Вниз\n← Влево\n→ Вправо",
            font=("Arial", 9),
            bg="#EDE0C8",
            fg="#666666",
            justify="left",
        )
        arrow_keys.pack(anchor="w", pady=(2, 0))

        # Центральная колонка - WASD
        center_column = tk.Frame(controls_frame, bg="#EDE0C8")
        center_column.pack(side="left", expand=True, padx=20)

        wasd_label = tk.Label(
            center_column,
            text="WASD:",
            font=("Arial", 10, "bold"),
            bg="#EDE0C8",
            fg="#776E65",
        )
        wasd_label.pack(anchor="w")

        wasd_keys = tk.Label(
            center_column,
            text="W - Вверх\nA - Влево\nS - Вниз\nD - Вправо",
            font=("Arial", 9),
            bg="#EDE0C8",
            fg="#666666",
            justify="left",
        )
        wasd_keys.pack(anchor="w", pady=(2, 0))

        # Правая колонка - русская раскладка
        right_column = tk.Frame(controls_frame, bg="#EDE0C8")
        right_column.pack(side="left", expand=True)

        russian_label = tk.Label(
            right_column,
            text="Русская:",
            font=("Arial", 10, "bold"),
            bg="#EDE0C8",
            fg="#776E65",
        )
        russian_label.pack(anchor="w")

        russian_keys = tk.Label(
            right_column,
            text="Ц - Вверх\nФ - Влево\nЫ - Вниз\nВ - Вправо",
            font=("Arial", 9),
            bg="#EDE0C8",
            fg="#666666",
            justify="left",
        )
        russian_keys.pack(anchor="w", pady=(2, 0))

        # Подсказка по тренажерам
        solver_tip = tk.Label(
            instruction_frame,
            text="💡 В тренажерах кликайте на пустые клетки для размещения двоек",
            font=("Arial", 9, "italic"),
            bg="#EDE0C8",
            fg="#8F7A66",
        )
        solver_tip.pack(pady=(10, 0))

        # Разделитель перед выходом
        separator2 = ttk.Separator(main_frame, orient="horizontal")
        separator2.pack(fill="x", pady=20)

        # Кнопка выхода
        exit_btn = tk.Button(
            main_frame,
            text="Выход",
            font=("Arial", 10),
            command=self.window.quit,
            bg="#BBADA0",
            fg="#FFFFFF",
            relief="flat",
        )
        exit_btn.pack(pady=5)

    def run_normal(self):
        """Запуск обычной версии игры"""
        self.window.withdraw()  # Скрыть хаб
        game_logic = NormalGame2048()
        app = Game2048UI(game_logic, "2048 - Normal")
        app.window.protocol("WM_DELETE_WINDOW", lambda: self.on_game_close(app))
        app.run()

    def run_easy(self):
        """Запуск легкой версии игры"""
        self.window.withdraw()
        game_logic = EasyGame2048()
        app = Game2048UI(game_logic, "2048 - Easy")
        app.window.protocol("WM_DELETE_WINDOW", lambda: self.on_game_close(app))
        app.run()

    def run_hard(self):
        """Запуск сложной версии игры"""
        self.window.withdraw()
        game_logic = HardGame2048()
        app = Game2048UI(game_logic, "2048 - Hard")
        app.window.protocol("WM_DELETE_WINDOW", lambda: self.on_game_close(app))
        app.run()

    def run_practice_slow(self):
        """Запуск медленного тренажера с подсказками"""
        self.window.withdraw()
        app = PracticeSlowUI()
        app.window.protocol("WM_DELETE_WINDOW", lambda: self.on_solver_close(app))
        app.run()

    def run_practice_fast(self):
        """Запуск быстрого тренажера с автоматическими ходами"""
        self.window.withdraw()
        app = PracticeFastUI()
        app.window.protocol("WM_DELETE_WINDOW", lambda: self.on_solver_close(app))
        app.run()

    def on_game_close(self, app):
        """
        Обработчик закрытия игрового окна
        Возвращает пользователя в главный хаб
        """
        app.window.destroy()
        self.window.deiconify()  # Показать хаб снова

    def on_solver_close(self, app):
        """
        Обработчик закрытия тренажера
        Возвращает пользователя в главный хаб
        """
        app.window.destroy()
        self.window.deiconify()

    def run(self):
        """Запуск главного цикла хаба"""
        self.window.mainloop()


if __name__ == "__main__":
    hub = MainHub()
    hub.run()
