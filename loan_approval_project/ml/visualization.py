import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from ml.utils import save_plot  # Імпортуємо утиліту для збереження графіків


class DataVisualization:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def plot_feature_importance(self, feature_importances, feature_names):
        # """
        # Показує важливість ознак.
        # """
        # plt.figure(figsize=(10, 6))
        # feature_df = pd.DataFrame({
        #     'Feature': feature_names,
        #     'Importance': feature_importances
        # })
        # feature_df = feature_df.sort_values(by='Importance', ascending=False)
        #
        # sns.barplot(x='Importance', y='Feature', data=feature_df)
        # plt.title('Feature Importance')
        if len(feature_importances) != len(feature_names):
            print(
                f"Попередження: кількість важливостей ({len(feature_importances)}) не співпадає з кількістю ознак ({len(feature_names)})")
            # Якщо довжини не співпадають, обрізаємо або додаємо значення, щоб привести їх до однакової довжини
            min_length = min(len(feature_importances), len(feature_names))
            feature_importances = feature_importances[:min_length]
            feature_names = feature_names[:min_length]

            # Створюємо DataFrame для важливості ознак
        feature_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': feature_importances
        })

        # Сортуємо ознаки за важливістю
        feature_df = feature_df.sort_values(by='Importance', ascending=False)

        # Візуалізація
        plt.figure(figsize=(10, 8))
        sns.barplot(x='Importance', y='Feature', data=feature_df)
        plt.title('Важливість ознак')
        plt.show()

        # Збереження графіка
        save_plot(plt, 'feature_importance.png')

    def plot_variable_distribution(self, column_name):
        """
        Показує розподіл значень для окремої змінної.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data[column_name], kde=True)
        plt.title(f'Distribution of {column_name}')

        # Збереження графіка
        save_plot(plt, f'distribution_{column_name}.png')

    def plot_boxplot(self, column_name):
        """
        Показує коробкову діаграму для змінної.
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=self.data[column_name])
        plt.title(f'Boxplot of {column_name}')

        # Збереження графіка
        save_plot(plt, f'boxplot_{column_name}.png')

    def plot_correlation_matrix(self):
        """
        Показує кореляційну матрицю між числовими ознаками.
        """
        plt.figure(figsize=(12, 8))
        corr_matrix = self.data.corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Correlation Matrix')

        # Збереження графіка
        save_plot(plt, 'correlation_matrix.png')

    def plot_target_vs_feature(self, target_column, feature_column):
        """
        Показує залежність між змінною та цільовою змінною.
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=self.data[target_column], y=self.data[feature_column])
        plt.title(f'{feature_column} vs {target_column}')

        # Збереження графіка
        save_plot(plt, f'{feature_column}_vs_{target_column}.png')
