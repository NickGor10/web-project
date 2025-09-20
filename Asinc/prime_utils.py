from typing import List
from concurrent.futures import ThreadPoolExecutor


class PrimeFinder:
    """Class to encapsulate logic for prime number detection and search."""

    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if number is prime."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    def find_primes_single_thread(self, start: int, end: int) -> List[int]:
        """Find all prime numbers in range [start, end] using a single thread."""
        return [n for n in range(start, end + 1) if self.is_prime(n)]

    def find_primes_multi_thread(self, start: int, end: int) -> List[int]:
        """Find all prime numbers in range [start, end] using two threads."""
        mid = (start + end) // 2
        ranges = [(start, mid), (mid + 1, end)]

        results: List[List[int]] = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(self.find_primes_single_thread, r[0], r[1]) for r in ranges]
            for future in futures:
                results.append(future.result())

        # Об'єднуємо та сортуємо результати (щоб порядок був правильний)
        return sorted(results[0] + results[1])
