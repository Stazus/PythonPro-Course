import multiprocessing
import threading
import time


def intensywne_obliczenia():
    return sum(i * i for i in range(20_000_000))


def sekwencyjnie():
    start = time.perf_counter()

    intensywne_obliczenia()
    intensywne_obliczenia()

    return time.perf_counter() - start


def watki():
    start = time.perf_counter()

    watek1 = threading.Thread(target=intensywne_obliczenia)
    watek2 = threading.Thread(target=intensywne_obliczenia)

    watek1.start()
    watek2.start()

    watek1.join()
    watek2.join()

    return time.perf_counter() - start


def procesy():
    start = time.perf_counter()

    proces1 = multiprocessing.Process(
        target=intensywne_obliczenia
    )
    proces2 = multiprocessing.Process(
        target=intensywne_obliczenia
    )

    proces1.start()
    proces2.start()

    proces1.join()
    proces2.join()

    return time.perf_counter() - start


if __name__ == "__main__":
    czas_sekwencyjny = sekwencyjnie()
    czas_watkow = watki()
    czas_procesow = procesy()

    print(
        f"Czas sekwencyjny: "
        f"{czas_sekwencyjny:.2f} s"
    )
    print(
        f"Czas dwóch wątków: "
        f"{czas_watkow:.2f} s"
    )
    print(
        f"Czas dwóch procesów: "
        f"{czas_procesow:.2f} s"
    )

    # Wnioski:
    # Przy zadaniach CPU-bound wątki zwykle nie przyspieszają
    # obliczeń w CPythonie z powodu GIL.
    #
    # GIL pozwala w danym momencie wykonywać kod Pythona
    # tylko jednemu wątkowi w obrębie procesu.
    #
    # Osobne procesy mają własne interpretery i własny GIL,
    # dlatego mogą wykonywać obliczenia równolegle
    # na różnych rdzeniach procesora.
