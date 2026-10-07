"""Завдання 1. Порівняння рандомізованого та детермінованого QuickSort."""

import random
import statistics
import time

import matplotlib

matplotlib.use("Agg")  # збереження графіка у файл без відкриття вікна
import matplotlib.pyplot as plt

SIZES = [10_000, 50_000, 100_000, 500_000]
REPEATS = 5


def _quick_sort(arr, choose_pivot):
    """Загальна реалізація QuickSort із триланковим розбиттям (<, =, >).

    Триланкове розбиття коректно обробляє дублікати, а функція choose_pivot
    визначає, як саме обирається опорний елемент.
    """
    if len(arr) <= 1:
        return arr

    pivot = choose_pivot(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]

    return _quick_sort(less, choose_pivot) + equal + _quick_sort(greater, choose_pivot)


def randomized_quick_sort(arr):
    """QuickSort, де опорний елемент обирається випадково."""
    return _quick_sort(arr, lambda a: a[random.randrange(len(a))])


def deterministic_quick_sort(arr):
    """QuickSort, де опорний елемент — середній елемент масиву."""
    return _quick_sort(arr, lambda a: a[len(a) // 2])


def measure(sort_func, arr, repeats=REPEATS):
    """Повертає середній час (с) сортування копії масиву за `repeats` запусків."""
    times = []
    for _ in range(repeats):
        data = arr.copy()
        start = time.perf_counter()
        sort_func(data)
        times.append(time.perf_counter() - start)
    return statistics.mean(times)


def plot_results(sizes, rand_times, det_times, filename="quicksort_comparison.png"):
    plt.figure(figsize=(9, 5.5))
    plt.plot(sizes, rand_times, marker="o", label="Рандомізований QuickSort")
    plt.plot(sizes, det_times, marker="s", label="Детермінований QuickSort")
    plt.xlabel("Розмір масиву")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння рандомізованого та детермінованого QuickSort")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()


def main():
    random.seed(42)
    rand_times, det_times = [], []

    for size in SIZES:
        arr = [random.randint(0, 1_000_000) for _ in range(size)]

        # Перевірка коректності сортування
        expected = sorted(arr)
        assert randomized_quick_sort(arr) == expected
        assert deterministic_quick_sort(arr) == expected

        t_rand = measure(randomized_quick_sort, arr)
        t_det = measure(deterministic_quick_sort, arr)
        rand_times.append(t_rand)
        det_times.append(t_det)

        print(f"Розмір масиву: {size}")
        print(f"   Рандомізований QuickSort: {t_rand:.4f} секунд")
        print(f"   Детермінований QuickSort: {t_det:.4f} секунд\n")

    # Таблиця результатів
    print(f"{'Розмір':>10} | {'Рандомізований, с':>18} | {'Детермінований, с':>18}")
    print("-" * 54)
    for size, tr, td in zip(SIZES, rand_times, det_times):
        print(f"{size:>10} | {tr:>18.4f} | {td:>18.4f}")

    plot_results(SIZES, rand_times, det_times)


if __name__ == "__main__":
    main()
