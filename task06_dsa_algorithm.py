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


def dsa_sign(message: int, private_key: int, public_key: tuple[int, int, int, int], k: int | None = None) -> tuple[int, int, int]:
    p, q, g, _ = public_key
    x = private_key

    while True:
        if k is None:
            k = random.randrange(1, q)
        r = pow(g, k, p) % q
        if r == 0:
            k = None
            continue

        k_inv = mod_inverse(k, q)
        s = (k_inv * (message + x * r)) % q
        if s == 0:
            k = None
            continue
        return r, s, k


def dsa_verify(message: int, signature: tuple[int, int], public_key: tuple[int, int, int, int]) -> tuple[bool, int]:
    p, q, g, y = public_key
    r, s = signature

    if not (0 < r < q and 0 < s < q):
        return False, -1

    w = mod_inverse(s, q)
    u1 = (message * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q

    return v == r, v


if __name__ == "__main__":
    print("=== Алгоритм DSA ===")
    message_hash = int(input("Введите хеш сообщения (число H): "))
    use_custom_k = input("Задать k вручную? (y/n): ").strip().lower()
    custom_k = int(input("Введите k: ")) if use_custom_k == "y" else None

    print("\n--- Генерация параметров ---")
    p, q, g = generate_dsa_parameters()
    print(f"p = {p} (простое)")
    print(f"q = {q} (простое, q | (p-1))")
    print(f"g = {g} (образующий подгруппы порядка q)")

    public_key, private_key = generate_dsa_keys(p, q, g)
    print(f"Закрытый ключ x = {private_key}")
    print(f"Открытый ключ y = g^x mod p = {g}^{private_key} mod {p} = {public_key[3]}")

    print("\n--- Создание подписи ---")
    r, s, k_used = dsa_sign(message_hash, private_key, public_key, k=custom_k)
    k_inv = mod_inverse(k_used, q)
    print(f"k = {k_used}")
    print(f"r = (g^k mod p) mod q = ({g}^{k_used} mod {p}) mod {q} = {pow(g, k_used, p)} mod {q} = {r}")
    print(f"k^(-1) mod q = {k_inv}")
    print(f"s = k^(-1) * (H + x*r) mod q = {k_inv} * ({message_hash} + {private_key}*{r}) mod {q} = {s}")
    print(f"Подпись: (r, s) = ({r}, {s})")

    print("\n--- Проверка подписи ---")
    w = mod_inverse(s, q)
    u1 = (message_hash * w) % q
    u2 = (r * w) % q
    print(f"w = s^(-1) mod q = {w}")
    print(f"u1 = H*w mod q = {message_hash}*{w} mod {q} = {u1}")
    print(f"u2 = r*w mod q = {r}*{w} mod {q} = {u2}")
    print(f"v = (g^u1 * y^u2 mod p) mod q")
    print(f"  g^u1 mod p = {g}^{u1} mod {p} = {pow(g, u1, p)}")
    print(f"  y^u2 mod p = {public_key[3]}^{u2} mod {p} = {pow(public_key[3], u2, p)}")
    valid, v = dsa_verify(message_hash, (r, s), public_key)
    print(f"  v = {v}")
    print(f"v == r ({v} == {r}): {valid}")

    tampered = int(input("\nВведите изменённый хеш для проверки: "))
    tampered_valid, tampered_v = dsa_verify(tampered, (r, s), public_key)
    print(f"Проверка с H = {tampered}: v = {tampered_v}, подпись верна: {tampered_valid}")
