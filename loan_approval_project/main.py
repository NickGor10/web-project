import pandas as pd
from ml.data_preprocessing import DataPreprocessor
from ml.data_analysis import DataAnalysis
from ml.correlation_analysis import CorrelationAnalysis
from ml.model_training import ModelTrainer
from ml.visualization import DataVisualization
from sklearn.pipeline import Pipeline

def main():
    # Зчитуємо дані
    file_path = 'data/loan_data.csv'
    preprocessor = DataPreprocessor(file_path)
    processed_data = preprocessor.preprocess_data()

    # Створюємо класифікатор та pipeline
    model_trainer = ModelTrainer(processed_data)
    pipeline = model_trainer.train_model()

    # Отримуємо важливість ознак з моделі
    classifier = pipeline.named_steps['classifier']  # Крок класифікатора
    importances = classifier.feature_importances_

    # Отримуємо назви ознак після трансформацій
    preprocessor = pipeline.named_steps['preprocessor']  # Крок препроцесора
    categorical_cols = processed_data.select_dtypes(include=['object']).columns
    numerical_cols = processed_data.select_dtypes(include=['int64', 'float64']).columns

    # Обробка категоріальних ознак (OneHotEncoder)
    if hasattr(preprocessor, 'transformers_'):
        categorical_transformer = preprocessor.transformers_[1][1]
        if isinstance(categorical_transformer, Pipeline):
            onehot = categorical_transformer.named_steps['onehot']
            # Отримуємо нові назви колонок після One-Hot Encoding
            categorical_columns = onehot.get_feature_names_out(categorical_cols)
        else:
            categorical_columns = categorical_cols
    else:
        categorical_columns = categorical_cols

    # Створюємо список всіх колонок після трансформацій
    all_columns = list(numerical_cols) + list(categorical_columns)

    # Виводимо важливість ознак
    analysis = DataAnalysis(processed_data)
    analysis.plot_feature_importance(pipeline)  # Передаємо pipeline замість importances та all_columns

    # Ініціалізація для візуалізації
    data = pd.read_csv(file_path)
    visualization = DataVisualization(data)
    visualization.plot_feature_importance(importances, all_columns)

if __name__ == "__main__":
    main()
