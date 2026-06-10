"""
Задание 5. Поиск наименьшего образующего (примитивного корня) поля GF(p).

GF(p) — конечное поле из p элементов: {0, 1, 2, ..., p-1}, p — простое.

Примитивный корень g:
    Его степени g^1, g^2, ..., g^(p-1) mod p
    дают ВСЕ ненулевые элементы поля (в каком-то порядке).

Проверка:
    g — примитивный корень, если для каждого простого делителя q числа (p-1):
        g^((p-1)/q) != 1 (mod p)
"""


def prime_factors(n: int) -> list[int]:
    """
    Разлагает число n на простые множители (без повторений).
    Например: 12 -> [2, 3], 30 -> [2, 3, 5]
    """
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2  # после 2 проверяем только нечётные
    if n > 1:
        factors.append(n)
    return factors


def is_primitive_root(g: int, p: int, verbose: bool = False) -> bool:
    """
    Проверяет, является ли g примитивным корнем по модулю p.

    Алгоритм:
        1. Найти простые делители q числа phi(p) = p-1
        2. Для каждого q проверить: g^((p-1)/q) mod p != 1
        3. Если все проверки пройдены — g примитивный корень
    """
    if g <= 1 or g >= p:
        return False

    phi = p - 1
    factors = prime_factors(phi)

    if verbose:
        print(f"  Проверка g = {g}: phi(p) = {phi}, простые делители phi: {factors}")

    for q in factors:
        exp = phi // q
        value = pow(g, exp, p)
        if verbose:
            print(f"    g^({phi}/{q}) = {g}^{exp} mod {p} = {value}", end="")
        if value == 1:
            if verbose:
                print(" = 1  -> g НЕ примитивный корень")
            return False
        if verbose:
            print(f" != 1  -> OK")

    if verbose:
        print(f"  g = {g} — примитивный корень!")
    return True


def find_smallest_generator(p: int, verbose: bool = False) -> int:
    """
    Находит наименьший примитивный корень в GF(p).
    Перебирает g = 2, 3, 4, ... пока не найдёт подходящий.
    """
    if not is_prime_simple(p):
        raise ValueError("p должно быть простым числом")

    if verbose:
        print(f"\nПоиск наименьшего образующего в GF({p}):")

    for g in range(2, p):
        if is_primitive_root(g, p, verbose=verbose):
            return g

    raise ValueError("Примитивный корень не найден")


def is_prime_simple(n: int) -> bool:
    """Простая проверка: делим n на все числа до sqrt(n)."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1 if d == 2 else 2
    return True


if __name__ == "__main__":
    print("=== Примитивный корень GF(p) ===")
    p = int(input("Введите простое число p: "))

    if not is_prime_simple(p):
        print(f"Ошибка: {p} не является простым числом")
    else:
        g = find_smallest_generator(p, verbose=True)

        print(f"\n--- Результат ---")
        print(f"Наименьший образующий: g = {g}")

        # Показываем все степени g — они должны покрыть все элементы 1..p-1
        print(f"\nСтепени g mod {p}:")
        powers = []
        for k in range(1, p):
            val = pow(g, k, p)
            powers.append(val)
            print(f"  g^{k} mod {p} = {val}")

        unique = sorted(set(powers))
        print(f"\nУникальные элементы: {unique}")
        print(f"Всего элементов: {len(unique)} (должно быть {p - 1})")
