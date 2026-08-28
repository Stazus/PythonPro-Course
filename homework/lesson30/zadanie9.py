import threading


suma_calkowita = 0
blokada = threading.Lock()


def sumuj_fragment(fragment):
    global suma_calkowita

    suma_fragmentu = sum(fragment)

    with blokada:
        suma_calkowita += suma_fragmentu


if __name__ == "__main__":
    liczby = list(range(1, 10_000_001))

    rozmiar = len(liczby) // 4

    fragmenty = [
        liczby[i * rozmiar:(i + 1) * rozmiar]
        for i in range(4)
    ]

    watki = []

    for fragment in fragmenty:
        watek = threading.Thread(
            target=sumuj_fragment,
            args=(fragment,),
        )
        watki.append(watek)
        watek.start()

    for watek in watki:
        watek.join()

    print(f"Suma całkowita: {suma_calkowita}")
    print(f"Suma kontrolna: {sum(liczby)}")
    print(
        "Czy wynik jest poprawny?",
        suma_calkowita == sum(liczby),
    )
