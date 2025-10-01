from ml.data_preprocessing import DataPreprocessor
from ml.data_analysis import DataAnalysis
from ml.correlation_analysis import CorrelationAnalysis
from ml.model_training import ModelTrainer



def main():
    # Зчитуємо дані
    file_path = 'data/loan_data.csv'
    preprocessor = DataPreprocessor(file_path)
    processed_data = preprocessor.preprocess_data()

    # Аналізуємо дані
    analysis = DataAnalysis(processed_data)
    print("Описова статистика даних:")
    print(analysis.describe_data())

    # Розподіл даних
    analysis.plot_data_distribution()

    # Аналіз кореляцій
    correlation = CorrelationAnalysis(processed_data)
    correlation.correlation_matrix()  # Створює графік кореляції

    # Тренуємо модель
    model_trainer = ModelTrainer(processed_data)
    pipeline = model_trainer.train_model()  # отримуємо trained pipeline

    # Виводимо важливість ознак
    analysis.plot_feature_importance(pipeline)  # передаємо pipeline


if __name__ == "__main__":
    main()
