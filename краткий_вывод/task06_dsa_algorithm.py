"""
Задание 6. Алгоритм цифровой подписи DSA.
Подпись (r, s), проверка через v == r.
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
    q = 11
    while True:
        if not is_prime(q):
            q += 2
            continue
        p = 2 * q + 1
        if is_prime(p):
            break
        q += 2
    h = 2
    while True:
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            break
        h += 1
    return p, q, g


def generate_dsa_keys(p: int, q: int, g: int, x: int | None = None) -> tuple[tuple[int, int, int, int], int]:
    if x is None:
        x = random.randrange(1, q)
    y = pow(g, x, p)
    return (p, q, g, y), x


def dsa_sign(message: int, private_key: int, public_key: tuple[int, int, int, int], k: int | None = None) -> tuple[int, int]:
    p, q, g, _ = public_key
    x = private_key
    while True:
        if k is None:
            k = random.randrange(1, q)
        r = pow(g, k, p) % q
        if r == 0:
            k = None
            continue
        s = (mod_inverse(k, q) * (message + x * r)) % q
        if s == 0:
            k = None
            continue
        return r, s


def dsa_verify(message: int, signature: tuple[int, int], public_key: tuple[int, int, int, int]) -> bool:
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
    print("=== Алгоритм DSA ===")
    message_hash = int(input("Введите хеш сообщения (H): "))
    use_custom_k = input("Задать k вручную? (y/n): ").strip().lower()
    custom_k = int(input("Введите k: ")) if use_custom_k == "y" else None

    p, q, g = generate_dsa_parameters()
    public_key, private_key = generate_dsa_keys(p, q, g)

    print(f"\nПараметры: p={p}, q={q}, g={g}")
    print(f"Закрытый ключ x = {private_key}")
    print(f"Открытый ключ y = {public_key[3]}")

    signature = dsa_sign(message_hash, private_key, public_key, k=custom_k)
    valid = dsa_verify(message_hash, signature, public_key)

    print(f"\nПодпись (r, s) = {signature}")
    print(f"Подпись верна: {valid}")

    tampered = int(input("\nВведите изменённый хеш: "))
    print(f"Проверка с H = {tampered}: {dsa_verify(tampered, signature, public_key)}")
