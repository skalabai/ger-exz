"""
Задание 8. Метод Полларда (p-1) для поиска нетривиального делителя
составного числа n.
"""

import math
import random


def pollard_p_minus_1_verbose(n: int, bound: int = 20) -> int | None:
    """Метод p-1 с пошаговым выводом."""
    print(f"\n--- Попытка: bound B = {bound} ---")

    if n % 2 == 0:
        print(f"{n} чётное -> делитель 2")
        return 2

    a = random.randrange(2, n - 1)
    print(f"Случайное основание a = {a}")
    print(f"Вычисляем a^(B!) mod {n}:")

    for j in range(2, bound + 1):
        prev_a = a
        a = pow(a, j, n)
        print(f"  шаг j={j}: a = a^{j} mod {n} = {prev_a}^{j} mod {n} = {a}")

    g = math.gcd(a - 1, n)
    print(f"\ngcd(a - 1, n) = gcd({a} - 1, {n}) = gcd({a - 1}, {n}) = {g}")

    if 1 < g < n:
        print(f"Найден нетривиальный делитель: {g}")
        return g

    print("Делитель не найден при данном bound")
    return None


if __name__ == "__main__":
    print("=== Метод Полларда (p-1) ===")
    n = int(input("Введите составное число n: "))
    bound = int(input("Введите верхнюю границу B (например, 20): "))

    print(f"\nИщем делитель числа n = {n}")
    factor = pollard_p_minus_1_verbose(n, bound)

    if factor:
        other = n // factor
        print(f"\n--- Результат ---")
        print(f"{n} = {factor} * {other}")
        print(f"Проверка: {factor} * {other} = {factor * other}")
    else:
        retry = input("\nПовторить с большим B? (y/n): ").strip().lower()
        if retry == "y":
            new_bound = int(input("Введите новый B: "))
            factor = pollard_p_minus_1_verbose(n, new_bound)
            if factor:
                other = n // factor
                print(f"\n{n} = {factor} * {other}")
