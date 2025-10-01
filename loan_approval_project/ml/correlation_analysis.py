import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime


class CorrelationAnalysis:
    def __init__(self, data):
        self.data = data
        self.graphs_folder = 'graphs'  # Папка для збереження графіків

        # Якщо папка не існує, створюємо її
        if not os.path.exists(self.graphs_folder):
            os.makedirs(self.graphs_folder)

    def correlation_matrix(self):
        # Фільтруємо лише числові стовпці
        numerical_data = self.data.select_dtypes(include=['float64', 'int64'])

        # Обчислюємо кореляцію для числових змінних
        corr_matrix = numerical_data.corr()

        # Візуалізуємо кореляцію за допомогою heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')

        # Генеруємо унікальне ім'я файлу за допомогою поточної дати та часу
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'correlation_matrix_{timestamp}.png'

        # Зберігаємо графік в папку з графіками
        file_path = os.path.join(self.graphs_folder, file_name)
        plt.savefig(file_path, bbox_inches='tight')

        # Виводимо графік на екран
        plt.show()

        # Виводимо повідомлення про збереження файлу
        print(f"Графік збережено в '{file_path}'")
