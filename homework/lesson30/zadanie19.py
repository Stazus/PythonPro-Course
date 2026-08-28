import time
import random
from concurrent.futures import ThreadPoolExecutor


def analizuj_sentyment(zdanie):
    # Symulacja czasu oczekiwania na odpowiedź API AI.
    time.sleep(random.uniform(0.5, 2.0))

    sentyment = random.choice([
        "Pozytywny",
        "Negatywny",
        "Neutralny",
    ])

    return zdanie, sentyment


if __name__ == "__main__":
    opinie = [
        "Produkt jest bardzo dobry.",
        "Nie jestem zadowolony z zakupu.",
        "Produkt spełnia moje oczekiwania.",
        "Jakość wykonania jest przeciętna.",
        "Zdecydowanie kupiłbym ponownie.",
        "Produkt dotarł uszkodzony.",
        "Cena jest odpowiednia do jakości.",
        "Nie polecam tego produktu.",
        "Jestem bardzo zadowolony.",
        "Produkt działa poprawnie.",
        "Obsługa była bardzo dobra.",
        "Towar nie spełnił moich oczekiwań.",
        "Produkt wygląda bardzo dobrze.",
        "Dostawa była szybka.",
        "Jakość mogłaby być lepsza.",
        "Nie mam żadnych zastrzeżeń.",
        "Produkt jest łatwy w użyciu.",
        "Cena jest zbyt wysoka.",
        "Zakup uważam za udany.",
        "Produkt jest przeciętny.",
    ]

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=5) as executor:
        wyniki = list(
            executor.map(analizuj_sentyment, opinie)
        )

    koniec = time.perf_counter()

    for zdanie, sentyment in wyniki:
        print(f"{sentyment}: {zdanie}")

    print(
        f"\nCzas wykonania: {koniec - start:.2f} s"
    )
