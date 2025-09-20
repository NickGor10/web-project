# Пошук простих чисел (однопоточно та багатопоточно)

## Опис
Програма знаходить усі прості числа у заданому діапазоні двома способами:
- **Однопоточний пошук** (`find_primes_single_thread`)
- **Багатопоточний пошук** (`find_primes_multi_thread`) з використанням `ThreadPoolExecutor`

## Структура проєкту
- `prime_utils.py` – логіка перевірки та пошуку простих чисел
- `main.py` – точка входу, запуск і порівняння часу виконання
- `tests/test_prime_utils.py` – тести для обох функцій
- `requirements.txt` – залежності (pytest)

## Встановлення та запуск
### 1. Створення віртуального середовища
```bash
python -m venv venv
venv\Scripts\activate  # Windows 
```
### 2. Встановлення залежностей
```bash
pip install -r requirements.txt
```
### 3. Перевірка функцій
```bash
pytest -q
```

### 4. Запуск основного аналізу
```bash
python main.py
```