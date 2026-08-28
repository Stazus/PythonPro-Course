import multiprocessing
import math


def oblicz_silnie():
    wynik = math.factorial(10)
    print(f"Silnia liczby 10 wynosi: {wynik}")


if __name__ == "__main__":
    proces = multiprocessing.Process(target=oblicz_silnie)

    proces.start()
    proces.join()

    print("Proces zakończył pracę.")
