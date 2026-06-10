"""
Задание 9. Операции на эллиптической кривой над конечным полем F_p.
Кривая: y^2 = x^3 + a*x + b (mod p).
Реализованы сложение точек и удвоение точки.
"""


class EllipticCurve:
    """Эллиптическая кривая над полем F_p."""

    def __init__(self, a: int, b: int, p: int):
        self.a = a % p
        self.b = b % p
        self.p = p
        # Проверка невырожденности: 4a^3 + 27b^2 != 0 (mod p)
        discriminant = (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)) % self.p
        if discriminant == 0:
            raise ValueError("Кривая вырождена (discriminant = 0)")

    def is_on_curve(self, point: tuple[int, int] | None) -> bool:
        """Проверяет, лежит ли точка на кривой. None — точка в бесконечности O."""
        if point is None:
            return True
        x, y = point
        lhs = pow(y, 2, self.p)
        rhs = (pow(x, 3, self.p) + self.a * x + self.b) % self.p
        return lhs == rhs

    def negate(self, point: tuple[int, int] | None) -> tuple[int, int] | None:
        """Противоположная точка: (x, y) -> (x, -y)."""
        if point is None:
            return None
        x, y = point
        return x, (-y) % self.p

    def add(self, p1: tuple[int, int] | None, p2: tuple[int, int] | None) -> tuple[int, int] | None:
        """
        Сложение двух точек P + Q на эллиптической кривой.
        None обозначает точку в бесконечности O (нейтральный элемент).
        """
        if p1 is None:
            return p2
        if p2 is None:
            return p1

        x1, y1 = p1
        x2, y2 = p2

        # P + (-P) = O
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        # Если P == Q, используем формулу удвоения
        if p1 == p2:
            return self.double(p1)

        # Разные точки: вычисляем угловой коэффициент lambda
        lam = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p

        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return x3, y3

    def double(self, point: tuple[int, int]) -> tuple[int, int] | None:
        """
        Удвоение точки P + P = 2P.
        """
        x, y = point
        if y == 0:
            return None  # касательная вертикальна -> результат O

        # lambda = (3*x^2 + a) / (2*y)
        lam = ((3 * x * x + self.a) * pow(2 * y, -1, self.p)) % self.p

        x3 = (lam * lam - 2 * x) % self.p
        y3 = (lam * (x - x3) - y) % self.p
        return x3, y3

    def scalar_mult(self, k: int, point: tuple[int, int]) -> tuple[int, int] | None:
        """
        Умножение точки на скаляр: k*P (метод двоичного разложения).
        """
        result = None  # начинаем с O
        addend = point

        while k > 0:
            if k & 1:
                result = self.add(result, addend)
            addend = self.double(addend)
            k >>= 1

        return result


if __name__ == "__main__":
    # Кривая secp256k1-подобная (упрощённая для демонстрации)
    # y^2 = x^3 + 2x + 2 (mod 17)
    curve = EllipticCurve(a=2, b=2, p=17)

    P = (5, 1)
    Q = (6, 3)

    print("Точка P:", P, "на кривой:", curve.is_on_curve(P))
    print("Точка Q:", Q, "на кривой:", curve.is_on_curve(Q))

    R = curve.add(P, Q)
    print("P + Q =", R)

    D = curve.double(P)
    print("2P =", D)

    kP = curve.scalar_mult(5, P)
    print("5P =", kP)
