"""
Задание 8. Метод Полларда (p-1) для факторизации.

Идея:
    Пусть p — простой делитель n, и все простые делители (p-1) не превышают B.
    Тогда (p-1) делит B!, и по малой теореме Ферма:
        a^(B!) ≡ 1 (mod p)
    Значит p делит gcd(a^(B!) - 1, n) — это и есть искомый делитель.

Алгоритм:
    1. Выбрать случайное a
    2. Вычислить a^(B!) mod n  (по шагам: a = a^2, a = a^3, ..., a = a^B)
    3. g = gcd(a - 1, n)
    4. Если 1 < g < n — нашли делитель
"""

import math
import random


def pollard_p_minus_1_verbose(n: int, bound: int = 20) -> int | None:
    """
    Ищет нетривиальный делитель n методом p-1 с пошаговым выводом.

    Параметры:
        n     — составное число
        bound — верхняя граница B (чем больше, тем выше шанс найти делитель)

    Возвращает:
        Найденный делитель или None
    """
    print(f"\n--- Попытка: bound B = {bound} ---")

    # Чётные числа делятся на 2
    if n % 2 == 0:
        print(f"{n} чётное -> делитель 2")
        return 2

    # Случайное основание 2 <= a < n
    a = random.randrange(2, n - 1)
    print(f"Случайное основание a = {a}")
    print(f"Вычисляем a^(B!) mod {n} по шагам (a = a^2, a = a^3, ..., a = a^B):")

    # Последовательно умножаем: a = a^2 mod n, a = a^3 mod n, ... a = a^B mod n
    # Это эквивалентно a^(B!) mod n
    for j in range(2, bound + 1):
        prev_a = a
        a = pow(a, j, n)
        print(f"  шаг j={j}: a = a^{j} mod {n} = {prev_a}^{j} mod {n} = {a}")

    # Ищем общий делитель с n
    g = math.gcd(a - 1, n)
    print(f"\ngcd(a - 1, n) = gcd({a} - 1, {n}) = gcd({a - 1}, {n}) = {g}")

    if 1 < g < n:
        print(f"Найден нетривиальный делитель: {g}")
        return g

    print("Делитель не найден при данном bound (попробуйте увеличить B)")
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
        # Предлагаем повторить с большим B
        retry = input("\nПовторить с большим B? (y/n): ").strip().lower()
        if retry == "y":
            new_bound = int(input("Введите новый B: "))
            factor = pollard_p_minus_1_verbose(n, new_bound)
            if factor:
                other = n // factor
                print(f"\n{n} = {factor} * {other}")
