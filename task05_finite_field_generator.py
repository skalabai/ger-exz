"""
Задание 5. Поиск наименьшего образующего (примитивного корня)
конечного поля GF(p), где p — простое число.
"""


def prime_factors(n: int) -> list[int]:
    """Разложение числа на простые множители (уникальные)."""
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def is_primitive_root(g: int, p: int) -> bool:
    """
    Проверяет, является ли g примитивным корнем по модулю p.
    g — примитивный корень, если g^((p-1)/q) != 1 mod p
    для каждого простого делителя q числа (p-1).
    """
    if g <= 1 or g >= p:
        return False

    # Нужно проверить показатели (p-1) / q для всех простых q | (p-1)
    phi = p - 1
    for q in prime_factors(phi):
        if pow(g, phi // q, p) == 1:
            return False
    return True


def find_smallest_generator(p: int) -> int:
    """
    Находит наименьший примитивный корень поля GF(p).
    Перебираем g = 2, 3, ... пока не найдём подходящий.
    """
    if not is_prime_simple(p):
        raise ValueError("p должно быть простым числом")

    for g in range(2, p):
        if is_primitive_root(g, p):
            return g

    raise ValueError("Примитивный корень не найден")


def is_prime_simple(n: int) -> bool:
    """Вспомогательная проверка простоты."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1 if d == 2 else 2
    return True


if __name__ == "__main__":
    primes = [7, 11, 23, 97]

    for p in primes:
        g = find_smallest_generator(p)
        print(f"GF({p}): наименьший образующий g = {g}")

        # Проверка: степени g дают все ненулевые элементы поля
        powers = sorted({pow(g, k, p) for k in range(1, p)})
        print(f"  Элементы, порождённые g: {powers}")
