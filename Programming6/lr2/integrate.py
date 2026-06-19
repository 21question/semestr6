#!/usr/bin/env python3
"""
Численное интегрирование методом левых прямоугольников.
"""

import math
import timeit
from typing import Callable
import unittest


def integrate(f: Callable[[float], float],
              a: float,
              b: float,
              *,
              n_iter: int = 100000) -> float:
    """
    Приближённое вычисление определённого интеграла.

    Аргументы:
        f : подынтегральная функция
        a : нижний предел
        b : верхний предел
        n_iter : количество шагов (по умолчанию 100000)

    Возвращает:
        float : значение интеграла
    """
    step = (b - a) / n_iter
    acc = 0.0
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


class TestIntegration(unittest.TestCase):
    def test_sin(self):
        res = integrate(math.sin, 0, math.pi/2, n_iter=100000)
        self.assertAlmostEqual(res, 1.0, places=4)

    def test_polynomial(self):
        res = integrate(lambda x: x**2, 0, 1, n_iter=100000)
        self.assertAlmostEqual(res, 1/3, places=4)

    def test_convergence(self):
        coarse = integrate(math.sin, 0, math.pi/2, n_iter=1000)
        fine = integrate(math.sin, 0, math.pi/2, n_iter=100000)
        self.assertLess(abs(fine - 1), abs(coarse - 1))


if __name__ == "__main__":
    print("=== Doctest ===")
    import doctest
    doctest.testmod(verbose=True)

    print("\n=== Unittest ===")
    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n=== Замер времени ===")
    for n in [10000, 100000, 1000000]:
        elapsed = timeit.timeit(
            lambda: integrate(math.sin, 0, math.pi/2, n_iter=n),
            number=1
        )
        print(f"n_iter={n}: {elapsed:.4f} сек")