"""
Задание 9. Операции на эллиптической кривой над конечным полем F_p.
Кривая: y^2 = x^3 + a*x + b (mod p).
"""


class EllipticCurve:
    def __init__(self, a: int, b: int, p: int):
        self.a = a % p
        self.b = b % p
        self.p = p
        discriminant = (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)) % self.p
        if discriminant == 0:
            raise ValueError("Кривая вырождена (discriminant = 0)")

    def is_on_curve(self, point: tuple[int, int] | None) -> bool:
        if point is None:
            return True
        x, y = point
        lhs = pow(y, 2, self.p)
        rhs = (pow(x, 3, self.p) + self.a * x + self.b) % self.p
        return lhs == rhs

    def add_verbose(self, p1: tuple[int, int] | None, p2: tuple[int, int] | None) -> tuple[int, int] | None:
        if p1 is None:
            print("P = O -> P + Q = Q")
            return p2
        if p2 is None:
            print("Q = O -> P + Q = P")
            return p1

        x1, y1 = p1
        x2, y2 = p2

        if x1 == x2 and (y1 + y2) % self.p == 0:
            print(f"P = ({x1},{y1}), Q = ({x2},{y2}) — противоположные точки -> P + Q = O")
            return None

        if p1 == p2:
            return self.double_verbose(p1)

        print(f"\nСложение P({x1},{y1}) + Q({x2},{y2}):")
        lam = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        print(f"  lambda = (y2-y1)/(x2-x1) mod p = ({y2}-{y1}) * ({x2}-{x1})^(-1) mod {self.p}")
        print(f"  lambda = {y2 - y1} * {pow(x2 - x1, -1, self.p)} mod {self.p} = {lam}")

        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        print(f"  x3 = lambda^2 - x1 - x2 mod p = {lam}^2 - {x1} - {x2} mod {self.p} = {x3}")
        print(f"  y3 = lambda*(x1-x3) - y1 mod p = {lam}*({x1}-{x3}) - {y1} mod {self.p} = {y3}")
        print(f"  P + Q = ({x3}, {y3})")
        return x3, y3

    def double_verbose(self, point: tuple[int, int]) -> tuple[int, int] | None:
        x, y = point
        if y == 0:
            print(f"2P: y = 0 -> результат O")
            return None

        print(f"\nУдвоение 2P, P = ({x},{y}):")
        lam = ((3 * x * x + self.a) * pow(2 * y, -1, self.p)) % self.p
        print(f"  lambda = (3x^2+a)/(2y) mod p = (3*{x}^2+{self.a})/(2*{y}) mod {self.p}")
        print(f"  lambda = {(3*x*x + self.a)} * {pow(2*y, -1, self.p)} mod {self.p} = {lam}")

        x3 = (lam * lam - 2 * x) % self.p
        y3 = (lam * (x - x3) - y) % self.p
        print(f"  x3 = lambda^2 - 2x mod p = {lam}^2 - 2*{x} mod {self.p} = {x3}")
        print(f"  y3 = lambda*(x-x3) - y mod p = {lam}*({x}-{x3}) - {y} mod {self.p} = {y3}")
        print(f"  2P = ({x3}, {y3})")
        return x3, y3

    def scalar_mult_verbose(self, k: int, point: tuple[int, int]) -> tuple[int, int] | None:
        print(f"\nУмножение {k}*P, P = {point} (двоичное разложение):")
        print(f"  k = {k} = {bin(k)}")
        result = None
        addend = point
        step = 0

        while k > 0:
            step += 1
            if k & 1:
                print(f"  шаг {step}: бит 1 -> добавляем {addend}")
                result = self.add(result, addend) if result else addend
                print(f"           результат = {result}")
            else:
                print(f"  шаг {step}: бит 0 -> пропуск")
            addend = self.double(addend) if addend else None
            if addend:
                print(f"           удваиваем: {addend}")
            k >>= 1

        print(f"  Итог: {result}")
        return result

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


if __name__ == "__main__":
    print("=== Операции на эллиптической кривой ===")
    a = int(input("Введите коэффициент a: "))
    b = int(input("Введите коэффициент b: "))
    p = int(input("Введите модуль p (простое): "))

    curve = EllipticCurve(a, b, p)
    disc = (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p
    print(f"\nКривая: y^2 = x^3 + {a}x + {b} (mod {p})")
    print(f"Дискриминант = 4a^3 + 27b^2 mod p = {disc}")

    print("\n--- Точка P ---")
    x1 = int(input("x1: "))
    y1 = int(input("y1: "))
    P = (x1, y1)
    lhs = pow(y1, 2, p)
    rhs = (pow(x1, 3, p) + a * x1 + b) % p
    print(f"Проверка: y^2 mod p = {lhs}, x^3+ax+b mod p = {rhs} -> на кривой: {lhs == rhs}")

    print("\n--- Точка Q ---")
    x2 = int(input("x2: "))
    y2 = int(input("y2: "))
    Q = (x2, y2)
    lhs2 = pow(y2, 2, p)
    rhs2 = (pow(x2, 3, p) + a * x2 + b) % p
    print(f"Проверка: y^2 mod p = {lhs2}, x^3+ax+b mod p = {rhs2} -> на кривой: {lhs2 == rhs2}")

    print("\n--- Операции ---")
    curve.add_verbose(P, Q)
    curve.double_verbose(P)

    k = int(input("\nВведите скаляр k для k*P: "))
    curve.scalar_mult_verbose(k, P)
