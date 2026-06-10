"""
Задание 5. Поиск наименьшего образующего (примитивного корня)
конечного поля GF(p), где p — простое число.
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


def is_primitive_root(g: int, p: int, verbose: bool = False) -> bool:
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
    if not is_prime_simple(p):
        raise ValueError("p должно быть простым числом")

    if verbose:
        print(f"\nПоиск наименьшего образующего в GF({p}):")

    for g in range(2, p):
        if is_primitive_root(g, p, verbose=verbose):
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
        print(f"Ошибка: {p} не является простым числом")
    else:
        g = find_smallest_generator(p, verbose=True)

        print(f"\n--- Результат ---")
        print(f"Наименьший образующий: g = {g}")

        print(f"\nСтепени g mod {p}:")
        powers = []
        for k in range(1, p):
            val = pow(g, k, p)
            powers.append(val)
            print(f"  g^{k} mod {p} = {val}")

        unique = sorted(set(powers))
        print(f"\nУникальные элементы: {unique}")
        print(f"Всего элементов: {len(unique)} (должно быть {p - 1})")
