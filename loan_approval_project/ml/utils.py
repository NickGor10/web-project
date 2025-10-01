import os
import matplotlib.pyplot as plt


def save_plot(fig, filename, directory="graphs"):
    """
    Зберігає графік у файл PNG в зазначену директорію.

    :param fig: Об'єкт графіка, що потрібно зберегти.
    :param filename: Ім'я файлу, з яким буде збережений графік.
    :param directory: Директорія, де зберігаються графіки (за замовчуванням - 'graphs').
    """
    # Перевірка наявності директорії, якщо її немає - створюємо
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Формуємо повний шлях до файлу
    file_path = os.path.join(directory, filename)

    # Зберігаємо графік
    fig.savefig(file_path, bbox_inches='tight', dpi=300)
    print(f"Графік збережено в {file_path}")