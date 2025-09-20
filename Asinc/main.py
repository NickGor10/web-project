import time
from prime_utils import PrimeFinder


def measure_time(func, *args):
    start_time = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start_time
    return result, elapsed


def main():
    prime_finder = PrimeFinder()
    ranges = [(1, 100_000), (1, 500_000)]  # робимо діапазони великими аби побачити різницю

    for start, end in ranges:
        single_result, single_time = measure_time(prime_finder.find_primes_single_thread, start, end)
        multi_result, multi_time = measure_time(prime_finder.find_primes_multi_thread, start, end)

        print(f"\nДіапазон [{start}, {end}]")
        print(f"  Однопоточний пошук: {len(single_result)} чисел, час {single_time:.4f} c")
        print(f"  Багатопоточний пошук: {len(multi_result)} чисел, час {multi_time:.4f} c")

        assert single_result == multi_result, "Результати не збігаються!"

        # Аналіз ефективності
        if multi_time < single_time:
            print(f"  → Багатопоточний метод швидший на {single_time - multi_time:.4f} c")
        else:
            print(f"  → Однопоточний метод швидший на {multi_time - single_time:.4f} c")

        print("  (Пояснення: для малих діапазонів накладні витрати потоків переважають, "
              "для великих діапазонів паралельне обчислення стає ефективнішим.)")


if __name__ == "__main__":
    main()
