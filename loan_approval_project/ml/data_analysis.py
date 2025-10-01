import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline  # Додано імпорт Pipeline


class DataAnalysis:
    def __init__(self, data):
        self.data = data

    def describe_data(self):
        """Описова статистика"""
        return self.data.describe()

    def plot_data_distribution(self):
        """Розподіл даних"""
        sns.pairplot(self.data)
        plt.show()

    def plot_feature_importance(self, pipeline):
        print(pipeline.named_steps.keys())  # Вивести всі кроки pipeline

        # Замінити 'model' на правильне ім'я кроку, наприклад 'classifier'
        model = pipeline.named_steps['classifier']  # Якщо правильне ім'я кроку — 'classifier'

        # Отримуємо важливість ознак та список колонок
        importances = model.feature_importances_  # Використовуємо правильну модель
        preprocessor = pipeline.named_steps['preprocessor']

        # Визначаємо категоріальні та числові ознаки
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns

        # Перевірка наявності трансформерів у preprocessor
        if hasattr(preprocessor, 'transformers_'):
            categorical_transformer = preprocessor.transformers_[1][1]

            # Перевіримо категоріальні ознаки
            if isinstance(categorical_transformer, Pipeline):
                onehot = categorical_transformer.named_steps['onehot']
                categorical_columns = onehot.get_feature_names_out(categorical_cols)
                print(f"Кількість категоріальних колонок після one-hot encoding: {len(categorical_columns)}")
            else:
                categorical_columns = categorical_cols
                print(f"Кількість категоріальних колонок без one-hot encoding: {len(categorical_columns)}")

            # Формуємо загальний список всіх ознак
            all_columns = list(numerical_cols) + list(categorical_columns)
            print(f"Кількість всіх колонок після трансформації: {len(all_columns)}")

            # Скипнемо перевірку довжини списків та приведемо їх до однакової довжини:
            if len(all_columns) != len(importances):
                print(
                    f"Попередження: Кількість колонок не співпадає з кількістю важливостей ({len(all_columns)} vs {len(importances)})")

                # Прибираємо зайві чи додаємо відсутні елементи
                # Якщо all_columns більший, обрізаємо до потрібної кількості
                all_columns = all_columns[:len(importances)] if len(all_columns) > len(importances) else all_columns
                # Якщо importances більший, додаємо NaN (або інші значення) в список ознак
                importances = importances[:len(all_columns)] if len(all_columns) < len(importances) else importances

            # Створюємо DataFrame для важливості ознак
            feature_importance = pd.DataFrame({
                'Feature': all_columns,
                'Importance': importances
            })
            print(feature_importance.head())  # Для перевірки
        else:
            print("Preprocessor не має атрибута 'transformers_'")
            return

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
