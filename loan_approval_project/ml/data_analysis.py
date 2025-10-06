import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline  # Додано імпорт Pipeline
import os


class DataAnalysis:
    def __init__(self, data):
        self.data = data

    def describe_data(self):
        """Описова статистика"""
        return self.data.describe()

    def plot_data_distribution(self):
        """Розподіл даних"""
        sns.pairplot(self.data)
        plt.title("Data Distribution")
        self.save_plot('data_distribution.png')
        plt.close()

    def plot_feature_importance(self, pipeline, feature_names):
        """Візуалізація важливості ознак"""
        print(f"Pipeline steps: {pipeline.named_steps.keys()}")

        # Отримуємо модель з pipeline
        model = pipeline.named_steps['classifier']

        # Отримуємо важливість ознак
        importances = model.feature_importances_

        # Отримуємо preprocessor
        preprocessor = pipeline.named_steps['preprocessor']

        # ВИПРАВЛЕННЯ: Отримуємо трансформовані назви колонок
        transformed_features = preprocessor.get_feature_names_out(feature_names)

        print(f"Кількість ознак після трансформації: {len(transformed_features)}")
        print(f"Кількість важливостей: {len(importances)}")

        # Перевірка відповідності
        if len(transformed_features) != len(importances):
            print(
                f"⚠️ Попередження: кількість важливостей ({len(importances)}) не співпадає з кількістю ознак ({len(transformed_features)})")
            return

        # Створюємо DataFrame для важливості ознак
        feature_importance = pd.DataFrame({
            'Feature': transformed_features,
            'Importance': importances
        })
        feature_importance = feature_importance.sort_values(by='Importance', ascending=False)

        # Візуалізація топ-20 найважливіших ознак
        plt.figure(figsize=(10, 8))
        top_features = feature_importance.head(20)
        sns.barplot(x='Importance', y='Feature', data=top_features)
        plt.title("Топ-20 найважливіших ознак")
        self.save_plot('feature_importance.png')
        plt.close()

        print(feature_importance.head(10))

    def plot_correlation_matrix(self):
        """Теплова карта кореляцій між ознаками"""
        corr_matrix = self.data.corr()  # Кореляція між числовими змінними
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Кореляційна матриця')
        self.save_plot('correlation_matrix.png')
        plt.close()

    def plot_class_distribution(self):
        """Аналіз розподілу класів цільової змінної"""
        plt.figure(figsize=(6, 4))
        sns.countplot(x='Loan_Status', data=self.data)
        plt.title('Розподіл класів цільової змінної (Loan_Status)')
        self.save_plot('class_distribution.png')
        plt.close()

    def save_plot(self, filename):
        """Збереження графіка в папку 'graphs'"""
        if not os.path.exists('graphs'):
            os.makedirs('graphs')  # Створення папки 'graphs', якщо вона не існує
        plt.savefig(f'graphs/{filename}', bbox_inches='tight')

