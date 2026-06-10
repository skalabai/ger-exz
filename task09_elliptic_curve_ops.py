"""
Задание 9. Операции на эллиптической кривой над конечным полем F_p.

Уравнение кривой: y^2 = x^3 + a*x + b  (mod p)

Точка O (бесконечность) — нейтральный элемент группы.

Сложение P + Q (P != Q):
    lambda = (y2 - y1) / (x2 - x1) mod p
    x3 = lambda^2 - x1 - x2 mod p
    y3 = lambda*(x1 - x3) - y1 mod p

Удвоение 2P:
    lambda = (3*x^2 + a) / (2*y) mod p
    x3 = lambda^2 - 2*x mod p
    y3 = lambda*(x - x3) - y mod p
"""


class EllipticCurve:
    """Эллиптическая кривая над полем F_p."""

    def __init__(self, a: int, b: int, p: int):
        """
        Создаёт кривую с коэффициентами a, b по модулю простого p.
        Проверяет, что кривая невырождена: 4a^3 + 27b^2 != 0 (mod p).
        """
        self.a = a % p
        self.b = b % p
        self.p = p
        discriminant = (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)) % self.p
        if discriminant == 0:
            raise ValueError("Кривая вырождена (discriminant = 0)")

    def is_on_curve(self, point: tuple[int, int] | None) -> bool:
        """Проверяет, лежит ли точка (x,y) на кривой. None = точка O — всегда на кривой."""
        if point is None:
            return True
        x, y = point
        lhs = pow(y, 2, self.p)                              # левая часть: y^2
        rhs = (pow(x, 3, self.p) + self.a * x + self.b) % self.p  # правая: x^3+ax+b
        return lhs == rhs

    def add_verbose(self, p1: tuple[int, int] | None, p2: tuple[int, int] | None) -> tuple[int, int] | None:
        """Сложение двух точек с подробным выводом формул."""
        # O + Q = Q (O — нейтральный элемент)
        if p1 is None:
            print("P = O -> P + Q = Q")
            return p2
        if p2 is None:
            print("Q = O -> P + Q = P")
            return p1

        x1, y1 = p1
        x2, y2 = p2

        # P + (-P) = O (противоположные точки)
        if x1 == x2 and (y1 + y2) % self.p == 0:
            print(f"P = ({x1},{y1}), Q = ({x2},{y2}) — противоположные точки -> P + Q = O")
            return None

        # Если P == Q, используем формулу удвоения
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
        """Удвоение точки 2P с подробным выводом."""
        x, y = point
        if y == 0:
            print(f"2P: y = 0 -> касательная вертикальна, результат O")
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
        """
        Умножение точки на скаляр k*P методом двоичного разложения.
        Аналог быстрого возведения в степень, но вместо умножения — сложение точек.
        """
        print(f"\nУмножение {k}*P, P = {point} (двоичное разложение):")
        print(f"  k = {k} = {bin(k)}")
        result = None   # начинаем с O
        addend = point  # текущая степень двойки * P
        step = 0

        while k > 0:
            step += 1
            if k & 1:  # если младший бит = 1, прибавляем addend
                print(f"  шаг {step}: бит 1 -> добавляем {addend}")
                result = self.add(result, addend) if result else addend
                print(f"           результат = {result}")
            else:
                print(f"  шаг {step}: бит 0 -> пропуск")
            addend = self.double(addend) if addend else None
            if addend:
                print(f"           удваиваем: {addend}")
            k >>= 1  # сдвигаем k вправо (следующий бит)

        print(f"  Итог: {result}")
        return result

    def add(self, p1, p2):
        """Сложение точек без вывода (для внутренних вычислений)."""
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
        """Удвоение точки без вывода."""
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
