from functions import divide, divide_three_numbers, get_element, get_two_elements

def run_tests():
    numbers = [10, 20, 30]

    print("=== Тести для divide ===")
    print("Тест: divide(10, 2)")
    print("Очікувано: 5.0")
    print("Результат:", divide(10, 2), "\n")

    print("Тест: divide(10, 0)")
    print("Очікувано: помилка ділення на нуль, None")
    print("Результат:", divide(10, 0), "\n")

    print("Тест: divide_three_numbers(12, 3, 0)")
    print("Очікувано: помилка ділення на нуль, None")
    print("Результат:", divide_three_numbers(12, 3, 0), "\n")

    print("Тест: divide_three_numbers(20, 4, 2)")
    print("Очікувано: 2.5")
    print("Результат:", divide_three_numbers(20, 4, 2), "\n")

    print("=== Тести для get_element ===")
    print("Тест: get_element(numbers, 1)")
    print("Очікувано: 20")
    print("Результат:", get_element(numbers, 1), "\n")

    print("Тест: get_element(numbers, 5)")
    print("Очікувано: помилка індексу, None")
    print("Результат:", get_element(numbers, 5), "\n")

    print("Тест: get_two_elements(numbers, 0, 2)")
    print("Очікувано: 40")
    print("Результат:", get_two_elements(numbers, 0, 2), "\n")

    print("Тест: get_two_elements(numbers, 0, 5)")
    print("Очікувано: помилка індексу, None")
    print("Результат:", get_two_elements(numbers, 0, 5), "\n")

if __name__ == "__main__":
    run_tests()