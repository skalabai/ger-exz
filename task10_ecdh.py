"""
Задание 10. Протокол обмена ключами Диффи—Хеллмана на эллиптических кривых (ECDH).
Стороны согласуют общий секретный ключ без передачи его по каналу.
"""


class EllipticCurve:
    """Эллиптическая кривая (используется в ECDH)."""

    def __init__(self, a: int, b: int, p: int):
        self.a = a % p
        self.b = b % p
        self.p = p

    def add(self, p1, p2):
        if p1 is None:
            return p2
        if p2 is None:
            return p1

        x1, y1 = p1
        x2, y2 = p2

        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        if p1 == p2:
            return self.double(p1)

        lam = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return x3, y3

    def double(self, point):
        x, y = point
        if y == 0:
            return None
        lam = ((3 * x * x + self.a) * pow(2 * y, -1, self.p)) % self.p
        x3 = (lam * lam - 2 * x) % self.p
        y3 = (lam * (x - x3) - y) % self.p
        return x3, y3

    def scalar_mult(self, k: int, point):
        result = None
        addend = point
        while k > 0:
            if k & 1:
                result = self.add(result, addend)
            addend = self.double(addend)
            k >>= 1
        return result


def derive_shared_secret(point) -> int:
    """
    Из общей точки на кривой извлекаем числовой ключ.
    В реальных системах берут x-координату и прогоняют через KDF (SHA-256 и т.д.).
    """
    if point is None:
        raise ValueError("Некорректная общая точка")
    return point[0]


def ecdh_key_exchange(curve: EllipticCurve, base_point, private_a: int, private_b: int):
    """
    Симуляция ECDH между Алисой и Бобом.
    - base_point G — общая базовая точка (публичный параметр кривой).
    - private_a, private_b — секретные ключи сторон.
    Возвращает общий секрет, вычисленный каждой стороной.
    """
    # Алиса отправляет Бобу A = a*G
    public_a = curve.scalar_mult(private_a, base_point)
    # Боб отправляет Алисе B = b*G
    public_b = curve.scalar_mult(private_b, base_point)

    # Алиса вычисляет S = a*B = a*b*G
    secret_alice = curve.scalar_mult(private_a, public_b)
    # Боб вычисляет S = b*A = b*a*G
    secret_bob = curve.scalar_mult(private_b, public_a)

    return public_a, public_b, derive_shared_secret(secret_alice), derive_shared_secret(secret_bob)


if __name__ == "__main__":
    # Параметры кривой y^2 = x^3 + 2x + 2 (mod 17)
    curve = EllipticCurve(a=2, b=2, p=17)
    G = (5, 1)  # базовая точка

    # Секретные ключи (в реальности — случайные большие числа)
    alice_private = 7
    bob_private = 13

    pub_a, pub_b, key_alice, key_bob = ecdh_key_exchange(
        curve, G, alice_private, bob_private
    )

    print("Базовая точка G:", G)
    print("Публичный ключ Алисы A = a*G:", pub_a)
    print("Публичный ключ Боба B = b*G:", pub_b)
    print("Общий секрет Алисы (x-координата):", key_alice)
    print("Общий секрет Боба (x-координата):", key_bob)
    print("Секреты совпали:", key_alice == key_bob)
