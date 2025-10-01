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

    def plot_feature_importance(self, pipeline):
        """Візуалізація важливості ознак"""
        print(f"Pipeline steps: {pipeline.named_steps.keys()}")  # Вивести всі кроки pipeline

        # Отримуємо модель з pipeline
        model = pipeline.named_steps['classifier']  # Потрібно вказати правильний крок у пайплайні

        # Отримуємо важливість ознак
        importances = model.feature_importances_

        # Перевіряємо, чи є preprocessor і як ми можемо отримати всі ознаки після трансформацій
        preprocessor = pipeline.named_steps['preprocessor']

        # Якщо є трансформери, отримуємо всі ознаки після one-hot encoding
        if hasattr(preprocessor, 'transformers_'):
            categorical_cols = self.data.select_dtypes(include=['object']).columns
            numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns

            if hasattr(preprocessor, 'transformers_'):
                # Отримуємо категоріальні ознаки після one-hot encoding
                categorical_transformer = preprocessor.transformers_[1][1]
                if isinstance(categorical_transformer, Pipeline):
                    onehot = categorical_transformer.named_steps['onehot']
                    categorical_columns = onehot.get_feature_names_out(categorical_cols)

                    # Всі ознаки після трансформації
                    all_columns = list(numerical_cols) + list(categorical_columns)
                    print(f"Кількість всіх колонок після трансформації: {len(all_columns)}")
                else:
                    categorical_columns = categorical_cols
                    all_columns = list(numerical_cols) + list(categorical_columns)

                # Перевіряємо відповідність кількості ознак і важливостей
                if len(all_columns) != len(importances):
                    print(f"Попередження: Кількість колонок не співпадає з кількістю важливостей ({len(all_columns)} vs {len(importances)})")
                    all_columns = all_columns[:len(importances)] if len(all_columns) > len(importances) else all_columns
                    importances = importances[:len(all_columns)] if len(all_columns) < len(importances) else importances

                # Створюємо DataFrame для важливості ознак
                feature_importance = pd.DataFrame({
                    'Feature': all_columns,
                    'Importance': importances
                })
                feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
                print(feature_importance.head())  # Перевірка
        else:
            print("Preprocessor не має атрибута 'transformers_'")
            return

        # Візуалізація
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=feature_importance)
        plt.title("Feature Importance")
        self.save_plot('feature_importance.png')
        plt.close()

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

