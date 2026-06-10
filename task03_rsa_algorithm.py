"""
Задание 3. Алгоритм RSA.

RSA — асимметричный алгоритм шифрования:
    - Открытый ключ (e, n) — для шифрования, можно всем
    - Закрытый ключ (d, n) — для расшифрования, только у владельца

Формулы:
    Шифрование:   c = m^e mod n
    Расшифрование: m = c^d mod n

Условие: сообщение m должно быть меньше модуля n.
"""


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Расширенный алгоритм Евклида.
    Находит НОД(a, b) и коэффициенты x, y: a*x + b*y = НОД(a, b).
    Используется для вычисления d = e^(-1) mod phi.
    """
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def mod_inverse(a: int, m: int) -> int:
    """Находит обратный элемент a^(-1) mod m."""
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m


def is_prime(n: int) -> bool:
    """Проверяет, является ли число простым."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def print_find_e(phi: int) -> int:
    """Ищет и выводит в консоль, как находим открытую экспоненту e."""
    print(f"\n[Поиск e] Открытая экспонента: число e, где НОД(e, phi) = 1")
    print(f"  phi = {phi}")
    e = 3
    while True:
        gcd, _, _ = extended_gcd(e, phi)
        if gcd == 1:
            print(f"  Пробуем e = {e}: НОД({e}, {phi}) = {gcd} -> ПОДХОДИТ")
            return e
        print(f"  Пробуем e = {e}: НОД({e}, {phi}) = {gcd} -> не подходит, e += 2")
        e += 2


def print_find_d(e: int, phi: int) -> int:
    """Ищет и выводит в консоль, как находим закрытую экспоненту d."""
    print(f"\n[Поиск d] Закрытая экспонента: d = e^(-1) mod phi")
    print(f"  Нужно найти d такое, что: e * d mod phi = 1")
    print(f"  То есть: {e} * d mod {phi} = 1")
    gcd, x, y = extended_gcd(e, phi)
    print(f"  Расширенный алгоритм Евклида для ({e}, {phi}):")
    print(f"    НОД = {gcd}, коэффициент x = {x}")
    d = x % phi
    print(f"  d = x mod phi = {x} mod {phi} = {d}")
    print(f"  Проверка: {e} * {d} mod {phi} = {e * d % phi}")
    return d


def generate_rsa_keys_verbose(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int], dict]:
    """Генерирует ключи RSA с подробным выводом поиска каждой переменной."""
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p и q должны быть простыми")
    if p == q:
        raise ValueError("p и q должны быть различными")

    print(f"\n[Ввод] p = {p} (простое), q = {q} (простое) — заданы пользователем")

    print(f"\n[Поиск n] Модуль RSA:")
    print(f"  Формула: n = p * q")
    n = p * q
    print(f"  n = {p} * {q} = {n}")

    print(f"\n[Поиск phi] Функция Эйлера:")
    print(f"  Формула: phi(n) = (p - 1) * (q - 1)")
    phi = (p - 1) * (q - 1)
    print(f"  phi = ({p}-1) * ({q}-1) = {p - 1} * {q - 1} = {phi}")

    e = print_find_e(phi)
    d = print_find_d(e, phi)

    print(f"\n[Итог ключей]")
    print(f"  Открытый ключ  (e, n) = ({e}, {n})")
    print(f"  Закрытый ключ (d, n) = ({d}, {n})")

    info = {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}
    return (e, n), (d, n), info


def rsa_encrypt(message: int, public_key: tuple[int, int]) -> int:
    """Шифрует: c = m^e mod n"""
    e, n = public_key
    if message >= n:
        raise ValueError("Сообщение должно быть меньше модуля n")
    return pow(message, e, n)


def rsa_decrypt(ciphertext: int, private_key: tuple[int, int]) -> int:
    """Расшифровывает: m = c^d mod n"""
    d, n = private_key
    return pow(ciphertext, d, n)


if __name__ == "__main__":
    print("=== Алгоритм RSA ===")
    p = int(input("Введите простое число p: "))
    q = int(input("Введите простое число q: "))
    message = int(input("Введите сообщение (число m): "))

    print("\n========== ГЕНЕРАЦИЯ КЛЮЧЕЙ ==========")
    public, private, info = generate_rsa_keys_verbose(p, q)

    if message >= info['n']:
        print(f"\nОшибка: m = {message} должно быть < n = {info['n']}")
        raise SystemExit(1)

    print(f"\n========== ШИФРОВАНИЕ ==========")
    print(f"[Поиск c] Шифротекст:")
    print(f"  Формула: c = m^e mod n")
    print(f"  c = {message}^{info['e']} mod {info['n']}")
    encrypted = rsa_encrypt(message, public)
    print(f"  c = {encrypted}")

    print(f"\n========== РАСШИФРОВАНИЕ ==========")
    print(f"[Поиск m] Расшифрованное сообщение:")
    print(f"  Формула: m = c^d mod n")
    print(f"  m = {encrypted}^{info['d']} mod {info['n']}")
    decrypted = rsa_decrypt(encrypted, private)
    print(f"  m = {decrypted}")
