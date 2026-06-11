"""
Задание 10. ECDH — обмен ключами на эллиптической кривой.
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


if __name__ == "__main__":
    print("=== ECDH ===")
    a = int(input("Коэффициент a: "))
    b = int(input("Коэффициент b: "))
    p = int(input("Модуль p: "))
    gx = int(input("G: x = "))
    gy = int(input("G: y = "))
    G = (gx, gy)

    alice = int(input("Секрет Алисы (a): "))
    bob = int(input("Секрет Боба (b): "))

    curve = EllipticCurve(a, b, p)

    A = curve.scalar_mult(alice, G)
    B = curve.scalar_mult(bob, G)
    S_alice = curve.scalar_mult(alice, B)
    S_bob = curve.scalar_mult(bob, A)

    print(f"\nПубличный ключ Алисы A = {A}")
    print(f"Публичный ключ Боба B = {B}")
    print(f"Общий секрет S = {S_alice}")
    print(f"Ключ (x-координата) = {S_alice[0]}")
    print(f"Секреты совпали: {S_alice == S_bob}")
