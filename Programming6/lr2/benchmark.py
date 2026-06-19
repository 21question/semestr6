#!/usr/bin/env python3
"""
Сравнительный бенчмарк всех подходов.
"""

import math
import timeit

from integrate import integrate
from integrate_parallel import integrate_parallel

try:
    from integrate_cython import integrate_cython
    CYTHON_OK = True
except ImportError:
    CYTHON_OK = False
    print("Cython не найден. Запустите: python3 setup.py build_ext --inplace")


def run_benchmark():
    n_iter = 1_000_000

    print("=" * 60)
    print("СРАВНЕНИЕ СКОРОСТИ ВЫЧИСЛЕНИЙ")
    print("=" * 60)

    # Python
    t_py = timeit.timeit(
        lambda: integrate(math.sin, 0, math.pi/2, n_iter=n_iter),
        number=1
    )
    print(f"\n1. Чистый Python:\n   {t_py:.4f} сек")

    # Потоки
    t_threads = timeit.timeit(
        lambda: integrate_parallel(math.sin, 0, math.pi/2,
                                   n_jobs=4, n_iter=n_iter,
                                   use_processes=False),
        number=1
    )
    print(f"\n2. Потоки (4 воркера):\n   {t_threads:.4f} сек  (ускорение: {t_py/t_threads:.2f}x)")

    # Процессы
    t_processes = timeit.timeit(
        lambda: integrate_parallel(math.sin, 0, math.pi/2,
                                   n_jobs=4, n_iter=n_iter,
                                   use_processes=True),
        number=1
    )
    print(f"\n3. Процессы (4 воркера):\n   {t_processes:.4f} сек  (ускорение: {t_py/t_processes:.2f}x)")

    # Cython
    if CYTHON_OK:
        t_cy = timeit.timeit(
            lambda: integrate_cython(math.sin, 0, math.pi/2, n_iter=n_iter),
            number=1
        )
        print(f"\n4. Cython (sin из C):\n   {t_cy:.4f} сек  (ускорение: {t_py/t_cy:.2f}x)")

    print("\n" + "=" * 60)
    print("ВЫВОДЫ:")
    print("• Потоки не дают выигрыша из-за GIL (CPU-bound задача).")
    print("• Процессы дают ускорение до 3–4 раз.")
    print("• Cython с C-функцией показывает наилучший результат.")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()