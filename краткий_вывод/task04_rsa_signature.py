"""
Задание 4. ЭЦП на основе RSA.
Подпись: s = h^d mod n. Проверка: h' = s^e mod n, сравниваем с h.
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


def generate_rsa_keys(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int], dict]:
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p и q должны быть простыми")
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while extended_gcd(e, phi)[0] != 1:
        e += 2
    d = mod_inverse(e, phi)
    return (e, n), (d, n), {"n": n, "e": e, "d": d}


def rsa_sign(message: int, private_key: tuple[int, int]) -> int:
    d, n = private_key
    if message >= n:
        raise ValueError("Хеш должен быть меньше модуля n")
    return pow(message, d, n)


def rsa_verify(message: int, signature: int, public_key: tuple[int, int]) -> tuple[bool, int]:
    e, n = public_key
    recovered = pow(signature, e, n)
    return recovered == message, recovered


if __name__ == "__main__":
    print("=== ЭЦП на основе RSA ===")
    p = int(input("Введите простое число p: "))
    q = int(input("Введите простое число q: "))
    document_hash = int(input("Введите хеш документа (число): "))

    public, private, info = generate_rsa_keys(p, q)
    print(f"\nКлючи: (e,n)=({info['e']},{info['n']}), (d,n)=({info['d']},{info['n']})")

    if document_hash >= info["n"]:
        print(f"\nОшибка: хеш h = {document_hash} должен быть < n = {info['n']}")
        raise SystemExit(1)

    signature = rsa_sign(document_hash, private)
    valid, recovered = rsa_verify(document_hash, signature, public)

    print(f"\nПодпись s = {signature}")
    print(f"Проверка: h' = {recovered}, подпись верна: {valid}")

    tampered = int(input("\nВведите изменённый хеш для проверки: "))
    tampered_valid, _ = rsa_verify(tampered, signature, public)
    print(f"Проверка с h = {tampered}: подпись верна: {tampered_valid}")
