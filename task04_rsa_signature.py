"""
Задание 4. Электронная цифровая подпись (ЭЦП) на основе RSA.

Принцип:
    - Подпись создаётся ЗАКРЫТЫМ ключом:  s = h^d mod n
    - Проверяется ОТКРЫТЫМ ключом:       h' = s^e mod n
    - Если h' == h, подпись верна
"""


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Расширенный алгоритм Евклида для нахождения обратного элемента."""
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


def print_find_e(phi: int) -> int:
    print(f"\n[Поиск e] Открытая экспонента e, где НОД(e, phi) = 1:")
    e = 3
    while True:
        gcd, _, _ = extended_gcd(e, phi)
        if gcd == 1:
            print(f"  e = {e}: НОД({e}, {phi}) = {gcd} -> ПОДХОДИТ")
            return e
        print(f"  e = {e}: НОД({e}, {phi}) = {gcd} -> не подходит")
        e += 2


def print_find_d(e: int, phi: int) -> int:
    print(f"\n[Поиск d] Закрытая экспонента d = e^(-1) mod phi:")
    print(f"  Условие: {e} * d mod {phi} = 1")
    gcd, x, _ = extended_gcd(e, phi)
    d = x % phi
    print(f"  Расширенный Евклид: d = {d}")
    print(f"  Проверка: {e} * {d} mod {phi} = {e * d % phi}")
    return d


def generate_rsa_keys_verbose(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int], dict]:
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p и q должны быть простыми")

    print(f"\n[Ввод] p = {p}, q = {q}")

    print(f"\n[Поиск n] n = p * q = {p} * {q} = {p * q}")
    n = p * q

    print(f"\n[Поиск phi] phi = (p-1)(q-1) = {p-1} * {q-1} = {(p-1)*(q-1)}")
    phi = (p - 1) * (q - 1)

    e = print_find_e(phi)
    d = print_find_d(e, phi)

    print(f"\n[Ключи] Открытый (e,n)=({e},{n}), Закрытый (d,n)=({d},{n})")
    return (e, n), (d, n), {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}


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
    document_hash = int(input("Введите хеш документа (число h): "))

    print("\n========== ГЕНЕРАЦИЯ КЛЮЧЕЙ ==========")
    public, private, info = generate_rsa_keys_verbose(p, q)

    if document_hash >= info['n']:
        print(f"\nОшибка: h = {document_hash} должен быть < n = {info['n']}")
        raise SystemExit(1)

    print(f"\n[Ввод] h = {document_hash} — хеш документа (задан пользователем)")

    print(f"\n========== СОЗДАНИЕ ПОДПИСИ ==========")
    print(f"[Поиск s] Подпись (закрытым ключом d):")
    print(f"  Формула: s = h^d mod n")
    print(f"  s = {document_hash}^{info['d']} mod {info['n']}")
    signature = rsa_sign(document_hash, private)
    print(f"  s = {signature}")

    print(f"\n========== ПРОВЕРКА ПОДПИСИ ==========")
    print(f"[Поиск h'] Восстановленный хеш (открытым ключом e):")
    print(f"  Формула: h' = s^e mod n")
    print(f"  h' = {signature}^{info['e']} mod {info['n']}")
    valid, recovered = rsa_verify(document_hash, signature, public)
    print(f"  h' = {recovered}")
    print(f"[Сравнение] h' == h ?  {recovered} == {document_hash} -> {valid}")

    tampered = int(input("\nВведите изменённый хеш для проверки подделки: "))
    print(f"\n[Проверка подделки] h_новый = {tampered}")
    print(f"  h' = s^e mod n = {signature}^{info['e']} mod {info['n']}")
    tampered_valid, tampered_recovered = rsa_verify(tampered, signature, public)
    print(f"  h' = {tampered_recovered} (не зависит от введённого h!)")
    print(f"  h' == h_новый ?  {tampered_recovered} == {tampered} -> {tampered_valid}")
