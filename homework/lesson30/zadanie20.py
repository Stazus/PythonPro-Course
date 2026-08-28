import multiprocessing
import random
import time


def zastosuj_filtr(obraz):
    wynik = []

    for wiersz in obraz:
        nowy_wiersz = []

        for piksel in wiersz:
            nowy_wiersz.append(piksel * 1.1)

        wynik.append(nowy_wiersz)

    return wynik


def utworz_obraz():
    return [
        [random.randint(0, 255) for _ in range(1000)]
        for _ in range(1000)
    ]


if __name__ == "__main__":
    print("Tworzenie 10 obrazów...")
    obrazy = [utworz_obraz() for _ in range(10)]

    print("Przetwarzanie sekwencyjne...")

    start = time.perf_counter()

    wyniki_sekwencyjne = [
        zastosuj_filtr(obraz)
        for obraz in obrazy
    ]

    koniec = time.perf_counter()

    czas_sekwencyjny = koniec - start

    print(
        f"Czas sekwencyjny: {czas_sekwencyjny:.2f} s"
    )

    print("Przetwarzanie równoległe...")

    start = time.perf_counter()

    with multiprocessing.Pool() as pool:
        wyniki_rownolegle = pool.map(
            zastosuj_filtr,
            obrazy,
        )

    koniec = time.perf_counter()

    czas_rownolegly = koniec - start

    print(
        f"Czas równoległy: {czas_rownolegly:.2f} s"
    )

    print(
        f"Przyspieszenie: "
        f"{czas_sekwencyjny / czas_rownolegly:.2f}x"
    )
