"""
Задание 8. Метод Полларда (p-1) для факторизации.
"""

import math
import random


def pollard_p_minus_1(n: int, bound: int = 20) -> int | None:
    if n % 2 == 0:
        return 2
    a = random.randrange(2, n - 1)
    for j in range(2, bound + 1):
        a = pow(a, j, n)
    g = math.gcd(a - 1, n)
    if 1 < g < n:
        return g
    return None


if __name__ == "__main__":
    print("=== Метод Полларда (p-1) ===")
    n = int(input("Введите составное число n: "))
    bound = int(input("Введите границу B: "))

    factor = pollard_p_minus_1(n, bound)

    if factor:
        other = n // factor
        print(f"\n{n} = {factor} * {other}")
    else:
        print("\nДелитель не найден. Попробуйте увеличить B.")
        retry = input("Повторить? (y/n): ").strip().lower()
        if retry == "y":
            new_bound = int(input("Новый B: "))
            factor = pollard_p_minus_1(n, new_bound)
            if factor:
                print(f"\n{n} = {factor} * {n // factor}")
