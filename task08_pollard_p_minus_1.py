"""
Задание 8. Метод Полларда (p-1) для поиска нетривиального делителя
составного числа n.
Идея: если p-1 делит B! для некоторого B, то a^(B!) ≡ 1 (mod p),
и gcd(a^(B!) - 1, n) может дать делитель p.
"""

import math
import random


def pollard_p_minus_1(n: int, bound: int = 20) -> int | None:
    """
    Ищет нетривиальный делитель числа n методом p-1.
    bound — верхняя граница B (чем больше, тем выше шанс найти делитель).
    """
    if n % 2 == 0:
        return 2

    a = random.randrange(2, n - 1)
    # Вычисляем a^(B!) mod n через последовательное возведение в степень
    for j in range(2, bound + 1):
        a = pow(a, j, n)

    g = math.gcd(a - 1, n)

    if 1 < g < n:
        return g

    return None


def factor_with_retries(n: int, max_bound: int = 50, attempts: int = 10) -> int | None:
    """
    Несколько попыток с разными параметрами и основаниями a.
    """
    for bound in range(10, max_bound + 1, 5):
        for _ in range(attempts):
            factor = pollard_p_minus_1(n, bound)
            if factor is not None:
                return factor
    return None


if __name__ == "__main__":
    # Примеры: числа вида p*q, где p-1 гладкое (много малых множителей)
    composite_numbers = [
        15,           # 3 * 5
        91,           # 7 * 13
        10403,        # 101 * 103
        3599,         # 59 * 61
    ]

    for n in composite_numbers:
        factor = factor_with_retries(n)
        if factor:
            other = n // factor
            print(f"n = {n}: найден делитель {factor}, другой делитель {other}")
        else:
            print(f"n = {n}: делитель не найден (попробуйте увеличить bound)")
