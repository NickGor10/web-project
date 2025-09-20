import pytest
from math_utils import add_numbers

def test_add_numbers():
    # Додатні числа
    assert add_numbers(3, 5) == 8
    # Від'ємні числа
    assert add_numbers(-2, -3) == -5
    # Додатнє та від'ємне
    assert add_numbers(5, -3) == 2
    # Додавання нуля
    assert add_numbers(0, 7) == 7
    assert add_numbers(10, 0) == 10
