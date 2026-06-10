"""
Задание 4. Электронная цифровая подпись (ЭЦП) на основе RSA.
Подпись создаётся закрытым ключом, проверяется открытым.
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


def generate_prime(bits: int) -> int:
    import random
    while True:
        candidate = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(candidate):
            return candidate


def generate_rsa_keys(bits: int = 16) -> tuple[tuple[int, int], tuple[int, int]]:
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while p == q:
        q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while extended_gcd(e, phi)[0] != 1:
        e += 2
    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def rsa_sign(message: int, private_key: tuple[int, int]) -> int:
    """
    Создание подписи: s = m^d mod n.
    Здесь message — числовой хеш документа (в реальности — хеш SHA и т.д.).
    """
    d, n = private_key
    if message >= n:
        raise ValueError("Хеш должен быть меньше модуля n")
    return pow(message, d, n)


def rsa_verify(message: int, signature: int, public_key: tuple[int, int]) -> bool:
    """
    Проверка подписи: вычисляем m' = s^e mod n и сравниваем с message.
    Если совпало — подпись верна.
    """
    e, n = public_key
    recovered = pow(signature, e, n)
    return recovered == message


if __name__ == "__main__":
    public, private = generate_rsa_keys(bits=16)

    # В учебном примере «хеш» — просто число
    document_hash = 12345

    signature = rsa_sign(document_hash, private)
    is_valid = rsa_verify(document_hash, signature, public)
    is_tampered = rsa_verify(document_hash + 1, signature, public)

    print("Хеш документа:", document_hash)
    print("Подпись:", signature)
    print("Подпись верна:", is_valid)
    print("Подпись при изменении хеша:", is_tampered)
