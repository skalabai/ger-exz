"""
Задание 9. Операции на эллиптической кривой y^2 = x^3 + ax + b (mod p).
"""


class EllipticCurve:
    def __init__(self, a: int, b: int, p: int):
        self.a = a % p
        self.b = b % p
        self.p = p
        disc = (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)) % self.p
        if disc == 0:
            raise ValueError("Кривая вырождена")

    def is_on_curve(self, point: tuple[int, int]) -> bool:
        x, y = point
        return pow(y, 2, self.p) == (pow(x, 3, self.p) + self.a * x + self.b) % self.p

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
    print("=== Операции на эллиптической кривой ===")
    a = int(input("Коэффициент a: "))
    b = int(input("Коэффициент b: "))
    p = int(input("Модуль p: "))

    curve = EllipticCurve(a, b, p)
    print(f"\nКривая: y^2 = x^3 + {a}x + {b} (mod {p})")

    x1, y1 = int(input("P: x = ")), int(input("P: y = "))
    x2, y2 = int(input("Q: x = ")), int(input("Q: y = "))
    P, Q = (x1, y1), (x2, y2)

    print(f"\nP на кривой: {curve.is_on_curve(P)}")
    print(f"Q на кривой: {curve.is_on_curve(Q)}")
    print(f"P + Q = {curve.add(P, Q)}")
    print(f"2P = {curve.double(P)}")

    k = int(input("\nСкаляр k для k*P: "))
    print(f"{k}*P = {curve.scalar_mult(k, P)}")
