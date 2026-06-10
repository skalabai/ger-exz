"""
Задание 7. Вероятностный тест простоты Миллера—Рабина.

Идея:
    Для простого n и случайного a: если n простое, то либо
        a^d ≡ 1 (mod n),  либо  a^(d*2^j) ≡ -1 (mod n)
    где n-1 = d * 2^r, d — нечётное.

    Если ни одно условие не выполнено — n составное (найден свидетель a).

Результат вероятностный: k раундов дают ошибку не более 4^(-k).
"""

import random


def miller_rabin_verbose(n: int, k: int = 10) -> bool:
    """
    Тест Миллера—Рабина с пошаговым выводом.

    Параметры:
        n — проверяемое число
        k — число раундов (больше k = надёжнее)

    Возвращает:
        True  — вероятно простое
        False — точно составное
    """
    # Малые числа обрабатываем отдельно
    if n < 2:
        print(f"{n} < 2 -> составное")
        return False
    if n in (2, 3):
        print(f"{n} — простое (малый простой)")
        return True
    if n % 2 == 0:
        print(f"{n} чётное -> составное")
        return False

    # Представляем n-1 = d * 2^r, где d нечётное
    print(f"\n[Поиск d и r] Разложение n-1 = d * 2^r (d — нечётное):")
    d = n - 1
    r = 0
    print(f"  Начало: d = n-1 = {n}-1 = {d}")
    while d % 2 == 0:
        print(f"  d = {d} чётное -> d = {d}//2 = {d // 2}, r = {r}+1 = {r + 1}")
        d //= 2
        r += 1
    print(f"  Итог: d = {d}, r = {r}  =>  n-1 = {d} * 2^{r} = {d * (2**r)}")
    print(f"Число раундов: {k}\n")

    # k независимых проверок
    for round_num in range(1, k + 1):
        a = random.randrange(2, n - 1)  # случайное основание
        x = pow(a, d, n)                 # x = a^d mod n

        print(f"--- Раунд {round_num} ---")
        print(f"Основание a = {a}")
        print(f"x = a^d mod n = {a}^{d} mod {n} = {x}")

        # Условие 1: a^d ≡ 1 (mod n) — продолжаем
        if x == 1 or x == n - 1:
            print(f"x = {x} -> продолжаем (возможно простое)")
            continue

        # Условие 2: ищем j такое что a^(d*2^j) ≡ -1 (mod n)
        composite = True
        for j in range(r - 1):
            prev_x = x
            x = pow(x, 2, n)  # возводим в квадрат: x -> x^2 mod n
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
    """Точная проверка делителями (для сравнения с Миллером-Рабином)."""
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

    print(f"\n[Ввод] n = {n}, k = {k} раундов")
    print(f"Проверяем число n = {n}")
    mr_result = miller_rabin_verbose(n, k)

    # Сравниваем с точным ответом
    exact = is_prime_deterministic_small(n)
    print(f"\n--- Сравнение ---")
    print(f"Миллер-Рабин: {'простое' if mr_result else 'составное'}")
    print(f"Точная проверка: {'простое' if exact else 'составное'}")
