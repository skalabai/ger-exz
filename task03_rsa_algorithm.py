"""
Задание 3. Алгоритм RSA.
Генерация ключей и шифрование/расшифрование числовых сообщений.
"""


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


def generate_rsa_keys_from_primes(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int], dict]:
    """Генерирует ключи RSA из заданных простых p и q."""
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p и q должны быть простыми")
    if p == q:
        raise ValueError("p и q должны быть различными")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 3
    while extended_gcd(e, phi)[0] != 1:
        e += 2

    d = mod_inverse(e, phi)

    info = {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}
    return (e, n), (d, n), info


def rsa_encrypt(message: int, public_key: tuple[int, int]) -> int:
    e, n = public_key
    if message >= n:
        raise ValueError("Сообщение должно быть меньше модуля n")
    return pow(message, e, n)


def rsa_decrypt(ciphertext: int, private_key: tuple[int, int]) -> int:
    d, n = private_key
    return pow(ciphertext, d, n)


if __name__ == "__main__":
    print("=== Алгоритм RSA ===")
    p = int(input("Введите простое число p: "))
    q = int(input("Введите простое число q: "))
    message = int(input("Введите сообщение (число m): "))

    print("\n--- Генерация ключей ---")
    public, private, info = generate_rsa_keys_from_primes(p, q)

    print(f"p = {info['p']}, q = {info['q']}")
    print(f"n = p * q = {info['p']} * {info['q']} = {info['n']}")
    print(f"phi(n) = (p-1)(q-1) = {p - 1} * {q - 1} = {info['phi']}")
    print(f"Открытая экспонента e = {info['e']}  (НОД(e, phi) = 1)")
    print(f"Закрытая экспонента d = {info['d']}  (e*d mod phi = {info['e'] * info['d'] % info['phi']})")
    print(f"Открытый ключ:  (e, n) = {public}")
    print(f"Закрытый ключ: (d, n) = {private}")

    if message >= info['n']:
        print(f"\nОшибка: сообщение m = {message} должно быть меньше n = {info['n']}")
        raise SystemExit(1)

    print("\n--- Шифрование ---")
    print(f"Формула: c = m^e mod n = {message}^{info['e']} mod {info['n']}")
    encrypted = rsa_encrypt(message, public)
    print(f"Шифротекст c = {encrypted}")

    print("\n--- Расшифрование ---")
    print(f"Формула: m = c^d mod n = {encrypted}^{info['d']} mod {info['n']}")
    decrypted = rsa_decrypt(encrypted, private)
    print(f"Расшифрованное сообщение m = {decrypted}")
