import pytest
from prime_utils import PrimeFinder

prime_finder = PrimeFinder()


def test_is_prime():
    assert prime_finder.is_prime(2) is True
    assert prime_finder.is_prime(3) is True
    assert prime_finder.is_prime(4) is False
    assert prime_finder.is_prime(13) is True
    assert prime_finder.is_prime(0) is False
    assert prime_finder.is_prime(1) is False


@pytest.mark.parametrize("start,end,expected", [
    (1, 10, [2, 3, 5, 7]),
    (10, 20, [11, 13, 17, 19]),
])
def test_find_primes_single_and_multi_thread(start, end, expected):
    single = prime_finder.find_primes_single_thread(start, end)
    multi = prime_finder.find_primes_multi_thread(start, end)
    assert single == expected
    assert single == multi  # Перевірка, що обидва методи дають однаковий результат
