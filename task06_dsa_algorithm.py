"""
Задание 6. Алгоритм цифровой подписи DSA (Digital Signature Algorithm).
Создание и проверка подписи для числового сообщения (хеша).
"""

import random


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    return gcd, y1, x1 - (a // b) * y1


def mod_inverse(a: int, m: int) -> int:
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1 if d == 2 else 2
    return True


def generate_dsa_parameters() -> tuple[int, int, int]:
    """
    Генерирует параметры DSA: простое p, простое q | (p-1), образующий g.
    Упрощённая учебная версия с небольшими числами.
    """
    # Ищем пару простых: p = k*q + 1, где q — простое и делит (p-1)
    q = 11
    while True:
        if not is_prime(q):
            q += 2
            continue
        p = 2 * q + 1
        if is_prime(p):
            break
        q += 2

    # Ищем g порядка q: g = h^((p-1)/q) mod p, h = 2, 3, ...
    h = 2
    while True:
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            break
        h += 1

    return p, q, g


def generate_dsa_keys(p: int, q: int, g: int) -> tuple[tuple[int, int, int, int], int]:
    """
    Генерирует ключи DSA.
    Закрытый ключ x, открытый y = g^x mod p.
    Возвращает (параметры+открытый ключ, закрытый ключ).
    """
    x = random.randrange(1, q)
    y = pow(g, x, p)
    public_key = (p, q, g, y)
    return public_key, x


def dsa_sign(message: int, private_key: int, public_key: tuple[int, int, int, int]) -> tuple[int, int]:
    """
    Создаёт подпись (r, s) для хеша message.
    """
    p, q, g, _ = public_key
    x = private_key

    while True:
        k = random.randrange(1, q)
        r = pow(g, k, p) % q
        if r == 0:
            continue

        k_inv = mod_inverse(k, q)
        s = (k_inv * (message + x * r)) % q
        if s == 0:
            continue
        return r, s


def dsa_verify(message: int, signature: tuple[int, int], public_key: tuple[int, int, int, int]) -> bool:
    """
    Проверяет подпись (r, s).
    """
    p, q, g, y = public_key
    r, s = signature

    if not (0 < r < q and 0 < s < q):
        return False

    w = mod_inverse(s, q)
    u1 = (message * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q

    return v == r


if __name__ == "__main__":
    p, q, g = generate_dsa_parameters()
    public_key, private_key = generate_dsa_keys(p, q, g)

    message_hash = 42

    signature = dsa_sign(message_hash, private_key, public_key)
    valid = dsa_verify(message_hash, signature, public_key)
    invalid = dsa_verify(message_hash + 1, signature, public_key)

    print("Параметры DSA: p =", p, ", q =", q, ", g =", g)
    print("Открытый ключ y =", public_key[3])
    print("Хеш сообщения:", message_hash)
    print("Подпись (r, s):", signature)
    print("Подпись верна:", valid)
    print("Подпись при подделке:", invalid)
