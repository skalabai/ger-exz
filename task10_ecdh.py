"""
Задание 10. Протокол обмена ключами ECDH на эллиптических кривых.

Идея (аналог Диффи-Хеллмана, но на ЭК):
    1. Алиса и Боб договариваются о кривой и базовой точке G (публично)
    2. Алиса выбирает секрет a, Боб — секрет b (никому не сообщают)
    3. Алиса отправляет A = a*G, Боб отправляет B = b*G
    4. Алиса вычисляет S = a*B = a*b*G
       Боб вычисляет   S = b*A = b*a*G  (то же самое!)
    5. Общий секрет — x-координата точки S

Безопасность: зная только A и B, сложно найти S (задача дискретного логарифма на ЭК).
"""


class EllipticCurve:
    """Эллиптическая кривая y^2 = x^3 + ax + b (mod p)."""

    def __init__(self, a: int, b: int, p: int):
        self.a = a % p
        self.b = b % p
        self.p = p

    def add(self, p1, p2):
        """Сложение двух точек на кривой."""
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        x1, y1 = p1
        x2, y2 = p2
        # Противоположные точки дают O
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None
        # P + P = 2P — формула удвоения
        if p1 == p2:
            return self.double(p1)
        lam = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return x3, y3

    def double(self, point):
        """Удвоение точки P -> 2P."""
        x, y = point
        if y == 0:
            return None
        lam = ((3 * x * x + self.a) * pow(2 * y, -1, self.p)) % self.p
        x3 = (lam * lam - 2 * x) % self.p
        y3 = (lam * (x - x3) - y) % self.p
        return x3, y3

    def scalar_mult(self, k: int, point):
        """
        Умножение точки на число k (k раз сложить точку с собой).
        Метод двоичного разложения — быстрый алгоритм.
        """
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
    Извлекает числовой ключ из общей точки S.
    Берём x-координату. В реальных системах ещё прогоняют через SHA-256 (KDF).
    """
    if point is None:
        raise ValueError("Некорректная общая точка")
    return point[0]


if __name__ == "__main__":
    print("=== ECDH (обмен ключами на ЭК) ===")

    # Параметры кривой (публичные, известны обеим сторонам)
    a = int(input("Введите коэффициент a: "))
    b = int(input("Введите коэффициент b: "))
    p = int(input("Введите модуль p: "))

    curve = EllipticCurve(a, b, p)
    print(f"\nКривая: y^2 = x^3 + {a}x + {b} (mod {p})")

    # Базовая точка G — публичный параметр
    gx = int(input("Базовая точка G: x = "))
    gy = int(input("Базовая точка G: y = "))
    G = (gx, gy)
    lhs = pow(gy, 2, p)
    rhs = (pow(gx, 3, p) + a * gx + b) % p
    print(f"G = {G}, на кривой: {lhs == rhs} (y^2={lhs}, x^3+ax+b={rhs})")

    # Секретные ключи — знает только каждая сторона
    alice_private = int(input("\nСекретный ключ Алисы (a): "))
    bob_private = int(input("Секретный ключ Боба (b): "))

    print("\n--- Шаг 1: публичные ключи (передаются по открытому каналу) ---")
    public_a = curve.scalar_mult(alice_private, G)  # A = a*G
    public_b = curve.scalar_mult(bob_private, G)    # B = b*G
    print(f"A = a*G = {alice_private}*{G} = {public_a}")
    print(f"B = b*G = {bob_private}*{G} = {public_b}")

    print("\n--- Шаг 2: вычисление общего секрета ---")
    secret_alice = curve.scalar_mult(alice_private, public_b)  # S = a*B
    secret_bob = curve.scalar_mult(bob_private, public_a)      # S = b*A
    print(f"Алиса: S = a*B = {alice_private}*{public_b} = {secret_alice}")
    print(f"Боб:   S = b*A = {bob_private}*{public_a} = {secret_bob}")

    # Извлекаем ключ из x-координаты общей точки
    key_alice = derive_shared_secret(secret_alice)
    key_bob = derive_shared_secret(secret_bob)
    print(f"\n--- Результат ---")
    print(f"Общий секрет Алисы (x-координата): {key_alice}")
    print(f"Общий секрет Боба (x-координата):  {key_bob}")
    print(f"Секреты совпали: {key_alice == key_bob}")
