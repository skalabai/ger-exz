"""
Задание 6. Алгоритм цифровой подписи DSA (Digital Signature Algorithm).

DSA создаёт подпись из двух чисел (r, s):

    Подписание (закрытый ключ x):
        r = (g^k mod p) mod q
        s = k^(-1) * (H + x*r) mod q

    Проверка (открытый ключ y = g^x mod p):
        w = s^(-1) mod q
        u1 = H*w mod q,  u2 = r*w mod q
        v = (g^u1 * y^u2 mod p) mod q
        Подпись верна, если v == r

Параметры: p, q — простые, q делит (p-1), g — образующий подгруппы порядка q.
"""

import random


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Расширенный алгоритм Евклида."""
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    return gcd, y1, x1 - (a // b) * y1


def mod_inverse(a: int, m: int) -> int:
    """Обратный элемент по модулю m."""
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m


def is_prime(n: int) -> bool:
    """Проверка на простоту."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1 if d == 2 else 2
    return True


def generate_dsa_parameters(verbose: bool = False) -> tuple[int, int, int]:
    """
    Генерирует параметры DSA: (p, q, g).
    Ищем простые p и q: p = 2q + 1, затем g = h^((p-1)/q) mod p.
    """
    if verbose:
        print("[Поиск q] Простое q, для которого p = 2q+1 тоже простое:")
    q = 11
    while True:
        if not is_prime(q):
            if verbose:
                print(f"  q = {q} — не простое, q += 2")
            q += 2
            continue
        p = 2 * q + 1
        if is_prime(p):
            if verbose:
                print(f"  q = {q}: p = 2*{q}+1 = {p} — простое -> ПОДХОДИТ")
            break
        if verbose:
            print(f"  q = {q}: p = {p} — не простое, q += 2")
        q += 2

    if verbose:
        print(f"\n[Поиск g] Образующий подгруппы: g = h^((p-1)/q) mod p")
    h = 2
    while True:
        exp = (p - 1) // q
        g = pow(h, exp, p)
        if verbose:
            print(f"  h = {h}: g = {h}^{exp} mod {p} = {g}", end="")
        if g > 1:
            if verbose:
                print(" -> g > 1, ПОДХОДИТ")
            break
        if verbose:
            print(" -> g = 1, пробуем h+1")
        h += 1

    return p, q, g


def generate_dsa_keys(p: int, q: int, g: int, x: int | None = None) -> tuple[tuple[int, int, int, int], int]:
    """
    Генерирует ключи DSA.
    x — закрытый ключ (случайное из [1, q-1])
    y = g^x mod p — открытый ключ
    """
    if x is None:
        x = random.randrange(1, q)
    y = pow(g, x, p)
    public_key = (p, q, g, y)
    return public_key, x


def dsa_sign(message: int, private_key: int, public_key: tuple[int, int, int, int], k: int | None = None) -> tuple[int, int, int]:
    """
    Создаёт подпись (r, s) для хеша message.
    k — одноразовое случайное число (критически важно для безопасности).
 
    Возвращает (r, s, k) — k возвращаем для демонстрации вычислений.
    """
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
    """
    Проверяет подпись (r, s).
    Возвращает (результат проверки, вычисленное v).
    """
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

    print("\n========== ГЕНЕРАЦИЯ ПАРАМЕТРОВ ==========")
    p, q, g = generate_dsa_parameters(verbose=True)
    print(f"\n[Итог] p={p}, q={q}, g={g}")

    print(f"\n[Поиск x] Закрытый ключ — случайное число из [1, q-1]:")
    public_key, private_key = generate_dsa_keys(p, q, g)
    print(f"  x = {private_key}")

    print(f"\n[Поиск y] Открытый ключ y = g^x mod p:")
    print(f"  y = {g}^{private_key} mod {p} = {pow(g, private_key, p)}")

    print(f"\n[Ввод] H = {message_hash} — хеш сообщения")

    print("\n========== СОЗДАНИЕ ПОДПИСИ ==========")
    r, s, k_used = dsa_sign(message_hash, private_key, public_key, k=custom_k)
    k_inv = mod_inverse(k_used, q)
    gk_mod_p = pow(g, k_used, p)
    print(f"[Поиск k] k = {k_used} (одноразовое случайное)")
    print(f"[Поиск r] r = (g^k mod p) mod q = ({g}^{k_used} mod {p}) mod {q} = {gk_mod_p} mod {q} = {r}")
    print(f"[Поиск k^(-1)] k^(-1) mod q = {k_inv}")
    inner = (message_hash + private_key * r) % q
    print(f"[Поиск s] s = k^(-1)*(H+x*r) mod q = {k_inv}*({message_hash}+{private_key}*{r}) mod {q}")
    print(f"         = {k_inv} * {inner} mod {q} = {s}")
    print(f"[Подпись] (r, s) = ({r}, {s})")

    print("\n========== ПРОВЕРКА ПОДПИСИ ==========")
    w = mod_inverse(s, q)
    u1 = (message_hash * w) % q
    u2 = (r * w) % q
    gu1 = pow(g, u1, p)
    yu2 = pow(public_key[3], u2, p)
    print(f"[Поиск w]  w = s^(-1) mod q = {w}")
    print(f"[Поиск u1] u1 = H*w mod q = {message_hash}*{w} mod {q} = {u1}")
    print(f"[Поиск u2] u2 = r*w mod q = {r}*{w} mod {q} = {u2}")
    print(f"[Поиск v]  v = (g^u1 * y^u2 mod p) mod q")
    print(f"  g^u1 mod p = {g}^{u1} mod {p} = {gu1}")
    print(f"  y^u2 mod p = {public_key[3]}^{u2} mod {p} = {yu2}")
    print(f"  v = ({gu1} * {yu2} mod {p}) mod {q}")
    valid, v = dsa_verify(message_hash, (r, s), public_key)
    print(f"  v = {v}")
    print(f"v == r ({v} == {r}): {valid}")

    tampered = int(input("\nВведите изменённый хеш для проверки: "))
    tampered_valid, tampered_v = dsa_verify(tampered, (r, s), public_key)
    print(f"Проверка с H = {tampered}: v = {tampered_v}, подпись верна: {tampered_valid}")
