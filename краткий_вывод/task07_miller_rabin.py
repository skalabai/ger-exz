"""
Задание 7. Тест простоты Миллера—Рабина.
"""

import random


def miller_rabin(n: int, k: int = 10) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True


def is_prime_deterministic(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1 if d == 2 else 2
    return True


if __name__ == "__main__":
    print("=== Тест Миллера—Рабина ===")
    n = int(input("Введите число n: "))
    k = int(input("Введите число раундов k: "))

    mr = miller_rabin(n, k)
    exact = is_prime_deterministic(n)

    print(f"\nМиллер—Рабин: {'простое' if mr else 'составное'}")
    print(f"Точная проверка: {'простое' if exact else 'составное'}")
