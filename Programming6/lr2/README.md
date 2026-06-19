# Лабораторная работа №2: Оптимизация численных методов

## Цель
Сравнить эффективность различных подходов к ускорению CPU-bound вычислений на примере численного интегрирования.

## Установка и запуск
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 setup.py build_ext --inplace
python3 benchmark.py
