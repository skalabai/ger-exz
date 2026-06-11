"""
Задание 5. Наименьший образующий (примитивный корень) поля GF(p).
"""


def prime_factors(n: int) -> list[int]:
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
    if g <= 1 or g >= p:
        return False
    phi = p - 1
    for q in prime_factors(phi):
        if pow(g, phi // q, p) == 1:
            return False
    return True


def find_smallest_generator(p: int) -> int:
    for g in range(2, p):
        if is_primitive_root(g, p):
            return g
    raise ValueError("Примитивный корень не найден")


def is_prime_simple(n: int) -> bool:
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
        print(f"Ошибка: {p} не является простым")
    else:
        g = find_smallest_generator(p)
        powers = sorted({pow(g, k, p) for k in range(1, p)})

        print(f"\nНаименьший образующий: g = {g}")
        print(f"Элементов, порождённых g: {len(powers)} из {p - 1}")
        print(f"Множество: {powers}")
