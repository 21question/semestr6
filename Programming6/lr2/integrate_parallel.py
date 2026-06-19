#!/usr/bin/env python3
"""
Параллельные реализации интегрирования: потоки и процессы.
"""

import math
import timeit
from typing import Callable
import concurrent.futures as ftres
from functools import partial


def integrate(f: Callable[[float], float],
              a: float,
              b: float,
              *,
              n_iter: int = 100000) -> float:
    step = (b - a) / n_iter
    acc = 0.0
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_parallel(f: Callable[[float], float],
                       a: float,
                       b: float,
                       *,
                       n_jobs: int = 2,
                       n_iter: int = 100000,
                       use_processes: bool = False) -> float:
    """
    Параллельное интегрирование с разбиением на подынтервалы.

    Аргументы:
        use_processes : True – процессы (ProcessPoolExecutor),
                        False – потоки (ThreadPoolExecutor)
    """
    step = (b - a) / n_jobs
    iter_per_job = n_iter // n_jobs

    Executor = ftres.ProcessPoolExecutor if use_processes else ftres.ThreadPoolExecutor

    with Executor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            left = a + i * step
            right = a + (i + 1) * step
            futures.append(executor.submit(integrate, f, left, right, n_iter=iter_per_job))

        total = 0.0
        for future in ftres.as_completed(futures):
            total += future.result()
        return total


if __name__ == "__main__":
    n_iter = 1_000_000

    print("=== Потоки (ThreadPoolExecutor) ===")
    for jobs in [2, 4, 6, 8]:
        t = timeit.timeit(
            lambda: integrate_parallel(math.sin, 0, math.pi/2,
                                       n_jobs=jobs, n_iter=n_iter,
                                       use_processes=False),
            number=1
        )
        print(f"n_jobs={jobs}: {t:.4f} сек")

    print("\n=== Процессы (ProcessPoolExecutor) ===")
    for jobs in [2, 4, 6, 8]:
        t = timeit.timeit(
            lambda: integrate_parallel(math.sin, 0, math.pi/2,
                                       n_jobs=jobs, n_iter=n_iter,
                                       use_processes=True),
            number=1
        )
        print(f"n_jobs={jobs}: {t:.4f} сек")