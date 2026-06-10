"""
Задание 3. Алгоритм RSA.
Генерация ключей и шифрование/расшифрование числовых сообщений.
"""


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Расширенный алгоритм Евклида.
    Возвращает (gcd, x, y), где gcd = a*x + b*y.
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
    """Простая проверка на простоту для небольших чисел."""
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
    """Генерирует простое число заданной битовой длины (упрощённо)."""
    import random
    while True:
        # Случайное нечётное число нужной длины
        candidate = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(candidate):
            return candidate


def generate_rsa_keys(bits: int = 16) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Генерирует пару ключей RSA.
    Возвращает ((e, n), (d, n)) — открытый и закрытый ключи.
    """
    # Выбираем два различных простых числа
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while p == q:
        q = generate_prime(bits // 2)

    n = p * q  # модуль
    phi = (p - 1) * (q - 1)  # функция Эйлера

    # Открытая экспонента: обычно 65537, для учебного примера — 3
    e = 3
    while extended_gcd(e, phi)[0] != 1:
        e += 2

    d = mod_inverse(e, phi)  # закрытая экспонента

    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


def rsa_encrypt(message: int, public_key: tuple[int, int]) -> int:
    """
    Шифрование: c = m^e mod n.
    message должно быть меньше n.
    """
    e, n = public_key
    if message >= n:
        raise ValueError("Сообщение должно быть меньше модуля n")
    return pow(message, e, n)


def rsa_decrypt(ciphertext: int, private_key: tuple[int, int]) -> int:
    """
    Расшифрование: m = c^d mod n.
    """
    d, n = private_key
    return pow(ciphertext, d, n)


if __name__ == "__main__":
    public, private = generate_rsa_keys(bits=16)
    print("Открытый ключ (e, n):", public)
    print("Закрытый ключ (d, n):", private)

    message = 42
    encrypted = rsa_encrypt(message, public)
    decrypted = rsa_decrypt(encrypted, private)

    print("\nСообщение:", message)
    print("Шифротекст:", encrypted)
    print("Расшифровано:", decrypted)
