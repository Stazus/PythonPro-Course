import multiprocessing
import random


def czy_pierwsza(liczba):
    if liczba < 2:
        return False

    for i in range(2, int(liczba ** 0.5) + 1):
        if liczba % i == 0:
            return False

    return True


if __name__ == "__main__":
    liczby = [random.randint(1, 1000) for _ in range(100)]

    with multiprocessing.Pool() as pool:
        wyniki = pool.map(czy_pierwsza, liczby)

    print("Wylosowane liczby:")
    print(liczby)

    print("\nWyniki True/False:")
    print(wyniki)

    liczba_pierwszych = sum(wyniki)

    print(f"\nLiczba znalezionych liczb pierwszych: {liczba_pierwszych}")
