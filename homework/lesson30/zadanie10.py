import glob
import threading


licznik = 0
blokada = threading.Lock()
szukane_slowo = "python"


def policz_slowo(nazwa_pliku):
    global licznik

    with open(nazwa_pliku, "r", encoding="utf-8") as plik:
        tekst = plik.read().lower()

    slowa = tekst.replace(".", "").replace(",", "").split()
    liczba = slowa.count(szukane_slowo)

    with blokada:
        licznik += liczba

    print(f"{nazwa_pliku}: {liczba}")


if __name__ == "__main__":
    pliki = glob.glob("*.txt")
    watki = []

    for nazwa_pliku in pliki:
        watek = threading.Thread(
            target=policz_slowo,
            args=(nazwa_pliku,),
        )
        watki.append(watek)
        watek.start()

    for watek in watki:
        watek.join()

    print(f"Łączna liczba wystąpień słowa '{szukane_slowo}': {licznik}")
