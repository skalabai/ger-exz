"""
Задание 10. Протокол обмена ключами Диффи—Хеллмана на эллиптических кривых (ECDH).
"""


class EllipticCurve:
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
    if point is None:
        raise ValueError("Некорректная общая точка")
    return point[0]


if __name__ == "__main__":
    print("=== ECDH (обмен ключами на ЭК) ===")

    a = int(input("Введите коэффициент a: "))
    b = int(input("Введите коэффициент b: "))
    p = int(input("Введите модуль p: "))

    curve = EllipticCurve(a, b, p)
    print(f"\nКривая: y^2 = x^3 + {a}x + {b} (mod {p})")

    gx = int(input("Базовая точка G: x = "))
    gy = int(input("Базовая точка G: y = "))
    G = (gx, gy)
    lhs = pow(gy, 2, p)
    rhs = (pow(gx, 3, p) + a * gx + b) % p
    print(f"G = {G}, на кривой: {lhs == rhs} (y^2={lhs}, x^3+ax+b={rhs})")

    alice_private = int(input("\nСекретный ключ Алисы (a): "))
    bob_private = int(input("Секретный ключ Боба (b): "))

    print("\n--- Шаг 1: публичные ключи ---")
    public_a = curve.scalar_mult(alice_private, G)
    public_b = curve.scalar_mult(bob_private, G)
    print(f"A = a*G = {alice_private}*{G} = {public_a}")
    print(f"B = b*G = {bob_private}*{G} = {public_b}")

    print("\n--- Шаг 2: общий секрет ---")
    secret_alice = curve.scalar_mult(alice_private, public_b)
    secret_bob = curve.scalar_mult(bob_private, public_a)
    print(f"Алиса: S = a*B = {alice_private}*{public_b} = {secret_alice}")
    print(f"Боб:   S = b*A = {bob_private}*{public_a} = {secret_bob}")

    key_alice = derive_shared_secret(secret_alice)
    key_bob = derive_shared_secret(secret_bob)
    print(f"\n--- Результат ---")
    print(f"Общий секрет Алисы (x-координата): {key_alice}")
    print(f"Общий секрет Боба (x-координата):  {key_bob}")
    print(f"Секреты совпали: {key_alice == key_bob}")
