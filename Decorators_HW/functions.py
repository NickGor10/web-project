from decorators import check_division_error, check_index_error

@check_division_error
def divide(a, b):
    """Ділення двох чисел."""
    return a / b

@check_division_error
def divide_three_numbers(a, b, c):
    """Ділення трьох чисел по черзі: a/b/c"""
    return a / b / c

@check_index_error
def get_element(lst, idx):
    """Повертає елемент списку за індексом."""
    return lst[idx]

@check_index_error
def get_two_elements(lst, idx1, idx2):
    """Повертає суму двох елементів списку за індексами."""
    return lst[idx1] + lst[idx2]