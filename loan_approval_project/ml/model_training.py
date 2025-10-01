import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score
import joblib
from ml.data_analysis import DataAnalysis


class ModelTrainer:
    def __init__(self, data):
        self.data = data
        self.X = self.data.drop('Loan_Status', axis=1)  # Всі стовпці, окрім цільової змінної
        self.y = self.data['Loan_Status']  # Цільова змінна (Loan_Status)


    def create_pipeline(self):
        # Трансформери для числових та категоріальних ознак
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # ColumnTransformer для комбінування трансформерів
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ])

        # Створення моделі Pipeline
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        return model

    def train_model(self):
        # Поділяємо дані на X (ознаки) і y (цільова змінна)
        X = self.data.drop('Loan_Status', axis=1)
        y = self.data['Loan_Status']

        # Створення трансформерів для числових та категоріальних ознак
        numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
        categorical_features = X.select_dtypes(include=['object']).columns

        # Трансформери для числових і категоріальних ознак
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Комбінуємо трансформери в ColumnTransformer
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )

        # Створюємо pipeline з класифікатором RandomForest
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier())
        ])

        # Пошук по сітці для налаштування параметрів
        param_grid = {
            'classifier__n_estimators': [100, 200],
            'classifier__max_depth': [None, 10, 20],
            'classifier__min_samples_split': [2, 5],
            'classifier__min_samples_leaf': [1, 2]
        }

        grid_search = GridSearchCV(model, param_grid, cv=5)
        grid_search.fit(X, y)

        print(f"Найкращі параметри: {grid_search.best_params_}")
        print(f"Найкраща оцінка на крос-валідації: {grid_search.best_score_}")

        return grid_search.best_estimator_  # Повертаємо готовий pipeline

    def cross_validate(self):
        model = self.create_pipeline()
        scores = cross_val_score(model, self.X, self.y, cv=5, scoring='accuracy')
        print(f"Оцінка моделі по крос-валідації: {scores.mean()}")
