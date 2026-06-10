"""
Задание 4. Электронная цифровая подпись (ЭЦП) на основе RSA.

Принцип:
    - Подпись создаётся ЗАКРЫТЫМ ключом:  s = h^d mod n
    - Проверяется ОТКРЫТЫМ ключом:       h' = s^e mod n
    - Если h' == h, подпись верна

Здесь h — хеш документа (число). В реальности сначала считают SHA-256 и берут mod n.
"""


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Расширенный алгоритм Евклида для нахождения обратного элемента."""
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    return gcd, y1, x1 - (a // b) * y1


def mod_inverse(a: int, m: int) -> int:
    """Вычисляет a^(-1) mod m."""
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m


def is_prime(n: int) -> bool:
    """Проверка числа на простоту."""
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
    """Генерирует ключи RSA (та же логика, что в задании 3)."""
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p и q должны быть простыми")
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while extended_gcd(e, phi)[0] != 1:
        e += 2
    d = mod_inverse(e, phi)
    return (e, n), (d, n), {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}


def rsa_sign(message: int, private_key: tuple[int, int]) -> int:
    """
    Создаёт цифровую подпись.
    Формула: s = h^d mod n  (подписываем закрытым ключом)
    """
    d, n = private_key
    if message >= n:
        raise ValueError("Хеш должен быть меньше модуля n")
    return pow(message, d, n)


def rsa_verify(message: int, signature: int, public_key: tuple[int, int]) -> tuple[bool, int]:
    """
    Проверяет цифровую подпись.
    Формула: h' = s^e mod n  (проверяем открытым ключом)
    Возвращает (True/False, восстановленный хеш h').
    """
    e, n = public_key
    recovered = pow(signature, e, n)
    return recovered == message, recovered


if __name__ == "__main__":
    print("=== ЭЦП на основе RSA ===")

    p = int(input("Введите простое число p: "))
    q = int(input("Введите простое число q: "))
    document_hash = int(input("Введите хеш документа (число): "))

    print("\n--- Генерация ключей ---")
    public, private, info = generate_rsa_keys_from_primes(p, q)
    print(f"n = {info['n']}, e = {info['e']}, d = {info['d']}")

    # Хеш должен быть меньше n — ограничение RSA
    if document_hash >= info['n']:
        print(f"\nОшибка: хеш h = {document_hash} должен быть меньше n = {info['n']}")
        print("Подсказка: введите хеш меньше n, например 10 при n=35")
        raise SystemExit(1)

    print("\n--- Создание подписи ---")
    print(f"Формула: s = h^d mod n = {document_hash}^{info['d']} mod {info['n']}")
    signature = rsa_sign(document_hash, private)
    print(f"Подпись s = {signature}")

    print("\n--- Проверка подписи (оригинальный хеш) ---")
    print(f"Формула: h' = s^e mod n = {signature}^{info['e']} mod {info['n']}")
    valid, recovered = rsa_verify(document_hash, signature, public)
    print(f"Восстановленный хеш h' = {recovered}")
    print(f"h' == h ({recovered} == {document_hash}): {valid}")

    # Демонстрация: при изменении хеша подпись не проходит проверку
    tampered = int(input("\nВведите изменённый хеш для проверки подделки: "))
    print(f"\n--- Проверка подписи (изменённый хеш {tampered}) ---")
    print(f"Формула: h' = s^e mod n = {signature}^{info['e']} mod {info['n']}")
    tampered_valid, tampered_recovered = rsa_verify(tampered, signature, public)
    print(f"Восстановленный хеш h' = {tampered_recovered}")
    print(f"h' == {tampered}: {tampered_valid}")
