"""
Задание 7. Вероятностный тест простоты Миллера—Рабина.
Проверяет, является ли число n простым, с заданной точностью.
"""


import random


def miller_rabin(n: int, k: int = 10) -> bool:
    """
    Тест Миллера—Рабина.
    n — проверяемое число, k — число раундов (больше k — выше надёжность).
    Возвращает True, если n вероятно простое, False — если составное.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Представляем n-1 как d * 2^r, где d нечётное
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # k независимых проверок со случайными основаниями
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        # Проверяем последовательность x^(2^j) mod n
        composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break

        if composite:
            return False

    return True


def is_prime_deterministic_small(n: int) -> bool:
    """Точная проверка для сравнения (малые числа)."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1 if d == 2 else 2
    return True


if __name__ == "__main__":
    test_numbers = [2, 17, 97, 100, 561, 1729, 104729, 1000003]

    print("Число\tМиллер-Рабин\tТочная проверка")
    print("-" * 45)
    for num in test_numbers:
        mr_result = miller_rabin(num)
        exact = is_prime_deterministic_small(num)
        status = "простое" if mr_result else "составное"
        print(f"{num}\t{status}\t\t{'простое' if exact else 'составное'}")
