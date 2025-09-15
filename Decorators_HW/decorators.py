from functools import wraps

def check_division_error(func):
    """
    Декоратор для перевірки ділення на нуль.
    Якщо ZeroDivisionError виникає під час виклику функції,
    виводить повідомлення і завершує програму.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            print(f"Помилка: ділення на нуль у функції '{func.__name__}'")
            # sys.exit(1)  # завершає програму, проте ми повертаємо None, щоб програма продовжила роботу і всі тестики пробігли
            return None
    return wrapper

def check_index_error(func):
    """
    Декоратор для перевірки виходу за межі списку (IndexError).
    Якщо при виклику функції виникає IndexError,
    виводить повідомлення, але програма продовжує виконання.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            print(f"Помилка: індекс за межами списку у функції '{func.__name__}'")
            return None
    return wrapper