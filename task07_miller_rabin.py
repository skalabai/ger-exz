"""
Задание 7. Вероятностный тест простоты Миллера—Рабина.
Проверяет, является ли число n простым, с заданной точностью.
"""

import random


def miller_rabin_verbose(n: int, k: int = 10) -> bool:
    """Тест Миллера—Рабина с пошаговым выводом."""
    if n < 2:
        print(f"{n} < 2 -> составное")
        return False
    if n in (2, 3):
        print(f"{n} — простое (малый простой)")
        return True
    if n % 2 == 0:
        print(f"{n} чётное -> составное")
        return False

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    print(f"\nn - 1 = {n - 1} = {d} * 2^{r}  (d = {d}, r = {r})")
    print(f"Число раундов: {k}\n")

    for round_num in range(1, k + 1):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        print(f"--- Раунд {round_num} ---")
        print(f"Основание a = {a}")
        print(f"x = a^d mod n = {a}^{d} mod {n} = {x}")

        if x == 1 or x == n - 1:
            print(f"x = {x} -> продолжаем (возможно простое)")
            continue

        composite = True
        for j in range(r - 1):
            prev_x = x
            x = pow(x, 2, n)
            print(f"  x = x^2 mod n = {prev_x}^2 mod {n} = {x}")
            if x == n - 1:
                print(f"  x = n-1 -> продолжаем")
                composite = False
                break

        if composite:
            print(f"Свидетель составности: a = {a}")
            print(f"ВЫВОД: {n} — СОСТАВНОЕ")
            return False

    print(f"\nВсе {k} раундов пройдены без свидетельства составности")
    print(f"ВЫВОД: {n} — вероятно ПРОСТОЕ")
    return True


def is_prime_deterministic_small(n: int) -> bool:
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
    n = int(input("Введите число n для проверки: "))
    k = int(input("Введите число раундов k (например, 5): "))

    print(f"\nПроверяем число n = {n}")
    mr_result = miller_rabin_verbose(n, k)

    exact = is_prime_deterministic_small(n)
    print(f"\n--- Сравнение ---")
    print(f"Миллер-Рабин: {'простое' if mr_result else 'составное'}")
    print(f"Точная проверка: {'простое' if exact else 'составное'}")
