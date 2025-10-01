import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline  # Додано імпорт Pipeline


class DataAnalysis:
    def __init__(self, data):
        self.data = data

    def describe_data(self):
        # Описова статистика
        return self.data.describe()

    def plot_data_distribution(self):
        # Розподіл даних
        sns.pairplot(self.data)
        plt.show()

    def plot_feature_importance(self, pipeline):
        model = pipeline.named_steps['classifier']  # 'classifier' це ім'я кроку в pipeline

        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_

            # Отримуємо трансформер з pipeline
            preprocessor = pipeline.named_steps['preprocessor']

            # Отримуємо список ознак після трансформацій
            categorical_cols = self.data.select_dtypes(include=['object']).columns
            numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns

            # Додаємо категоріальні ознаки після one-hot кодування
            categorical_transformer = preprocessor.transformers_[1][1]

            # Перевіримо, чи є OneHotEncoder, і витягнемо ознаки після кодування
            if isinstance(categorical_transformer, Pipeline):
                onehot = categorical_transformer.named_steps['onehot']
                categorical_columns = onehot.get_feature_names_out(categorical_cols)
            else:
                categorical_columns = categorical_cols

            # Тепер створюємо загальний список всіх ознак після трансформації
            all_columns = list(numerical_cols) + list(categorical_columns)

            # Перевіряємо чи співпадають довжини
            if len(importances) != len(all_columns):
                print(f"Увага! Довжина списків не співпадає: {len(importances)} vs {len(all_columns)}")

            # Створюємо DataFrame для важливості ознак
            feature_importance = pd.DataFrame({
                'Feature': all_columns,
                'Importance': importances
            })
            feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Importance', y='Feature', data=feature_importance)
            plt.title('Feature Importance')
            plt.show()

        else:
            print(f"Модель {type(model).__name__} не має атрибуту 'feature_importances_'")

    def plot_correlation_matrix(self):
        """Теплова карта кореляцій між ознаками"""
        corr_matrix = self.data.corr()  # Кореляція між числовими змінними
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Кореляційна матриця')
        plt.show()

    def plot_class_distribution(self):
        """Аналіз розподілу класів цільової змінної"""
        plt.figure(figsize=(6, 4))
        sns.countplot(x='Loan_Status', data=self.data)
        plt.title('Розподіл класів цільової змінної (Loan_Status)')
        plt.show()
