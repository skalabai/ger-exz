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
    Находит НОД(a, b) и коэффициенты x, y такие что: a*x + b*y = НОД(a, b).
    Нужен для вычисления обратного элемента d = e^(-1) mod phi(n).
    """
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def mod_inverse(a: int, m: int) -> int:
    """
    Находит обратный элемент a^(-1) mod m.
    Существует только если НОД(a, m) = 1.
    """
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m


def is_prime(n: int) -> bool:
    """Проверяет, является ли число простым (перебор делителей до sqrt(n))."""
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
    """
    Генерирует пару ключей RSA из двух простых чисел p и q.

    Шаги:
        1. n = p * q           — модуль
        2. phi = (p-1)(q-1)    — функция Эйлера
        3. e — открытая экспонента (НОД(e, phi) = 1)
        4. d = e^(-1) mod phi  — закрытая экспонента
    """
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p и q должны быть простыми")
    if p == q:
        raise ValueError("p и q должны быть различными")

    n = p * q                    # модуль RSA
    phi = (p - 1) * (q - 1)     # функция Эйлера: сколько чисел взаимно просто с n

    # Ищем e: начинаем с 3, берём нечётные, пока НОД(e, phi) != 1
    e = 3
    while extended_gcd(e, phi)[0] != 1:
        e += 2

    # d — число, что e*d ≡ 1 (mod phi)
    d = mod_inverse(e, phi)

    info = {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}
    return (e, n), (d, n), info


def rsa_encrypt(message: int, public_key: tuple[int, int]) -> int:
    """
    Шифрует сообщение открытым ключом.
    Формула: c = m^e mod n
    """
    e, n = public_key
    if message >= n:
        raise ValueError("Сообщение должно быть меньше модуля n")
    return pow(message, e, n)


def rsa_decrypt(ciphertext: int, private_key: tuple[int, int]) -> int:
    """
    Расшифровывает шифротекст закрытым ключом.
    Формула: m = c^d mod n
    """
    d, n = private_key
    return pow(ciphertext, d, n)


if __name__ == "__main__":
    print("=== Алгоритм RSA ===")

    # Пользователь вводит простые числа и сообщение
    p = int(input("Введите простое число p: "))
    q = int(input("Введите простое число q: "))
    message = int(input("Введите сообщение (число m): "))

    print("\n--- Генерация ключей ---")
    public, private, info = generate_rsa_keys_from_primes(p, q)

    # Подробный вывод всех промежуточных значений
    print(f"p = {info['p']}, q = {info['q']}")
    print(f"n = p * q = {info['p']} * {info['q']} = {info['n']}")
    print(f"phi(n) = (p-1)(q-1) = {p - 1} * {q - 1} = {info['phi']}")
    print(f"Открытая экспонента e = {info['e']}  (НОД(e, phi) = 1)")
    print(f"Закрытая экспонента d = {info['d']}  (e*d mod phi = {info['e'] * info['d'] % info['phi']})")
    print(f"Открытый ключ:  (e, n) = {public}")
    print(f"Закрытый ключ: (d, n) = {private}")

    # RSA работает только когда m < n
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
