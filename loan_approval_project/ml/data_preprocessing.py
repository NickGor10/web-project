import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

class DataPreprocessor:
    def __init__(self, file_path):
        # Завантажуємо дані з CSV
        self.data = pd.read_csv(file_path)

    def handle_missing_data(self):
        # Крок 1: Рахуємо пропущені значення
        missing_data_count = self.data.isnull().sum().sum()
        total_data_count = self.data.size
        missing_percentage = (missing_data_count / total_data_count) * 100

        print(f"Пропущено значень: {missing_data_count}/{total_data_count} ({missing_percentage:.2f}%)")

        # Якщо пропущені значення менше 20% від усіх даних
        if missing_percentage < 20:
            print("Менше 20% пропущених значень, видаляємо рядки з пропущеними даними.")
            self.data.dropna(inplace=True)
        else:
            print("Більше 20% пропущених значень, обробляємо по-іншому.")
            # Крок 2: Видаляти рядки з критичними пропущеними значеннями
            critical_columns = ['Loan_Status']  # Критичні колонки для аналізу
            self.data.dropna(subset=critical_columns, inplace=True)

            # Крок 3: Заповнення пропущених значень для інших колонок
            # Числові стовпці — заповнюємо середнім значенням
            numeric_cols = self.data.select_dtypes(include=['float64', 'int64']).columns
            self.data[numeric_cols] = self.data[numeric_cols].fillna(self.data[numeric_cols].mean())

            # Категоріальні стовпці — заповнюємо найбільш частим значенням
            categorical_cols = self.data.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                most_frequent = self.data[col].mode()[0]
                self.data[col] = self.data[col].fillna(most_frequent)

    def encode_categorical_data(self):
        """
        Кодуємо категоріальні змінні за допомогою LabelEncoder.
        Замість одного кодування для кожної змінної можна використовувати цикл для економії коду.
        """
        label_encoder = LabelEncoder()

        categorical_cols = ['Gender', 'Married', 'Self_Employed', 'Property_Area', 'Loan_Status']
        for col in categorical_cols:
            self.data[col] = label_encoder.fit_transform(self.data[col])

    def scale_numerical_data(self):
        """
        Масштабуємо числові змінні за допомогою StandardScaler.
        Це допомагає моделі бути менш чутливою до масштабу змінних, особливо для алгоритмів, які чутливі до масштабу (наприклад, логістична регресія).
        """
        scaler = StandardScaler()
        numerical_columns = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
        self.data[numerical_columns] = scaler.fit_transform(self.data[numerical_columns])

    def preprocess_data(self):
        """
        Основний метод для попередньої обробки даних:
        - Обробка пропущених значень
        - Кодування категоріальних змінних
        - Масштабування числових даних
        """
        self.handle_missing_data()  # Обробка пропущених значень
        self.encode_categorical_data()  # Кодування категоріальних змінних
        self.scale_numerical_data()  # Масштабування числових змінних
        return self.data
