while True:
    wejscie1 = input("Podaj pierwszą liczbę lub wpisz 'koniec', aby zakończyć: ")

    if wejscie1.lower() == "koniec":
        print("Koniec działania kalkulatora.")
        break

    try:
        liczba1 = float(wejscie1)
    except ValueError:
        print("Błąd: pierwsza liczba nie jest prawidłowa.\n")
        continue

    wejscie2 = input("Podaj drugą liczbę: ")

    try:
        liczba2 = float(wejscie2)
    except ValueError:
        print("Błąd: druga liczba nie jest prawidłowa.\n")
        continue

    print("Wynik dodawania:", liczba1 + liczba2)
    print("Wynik odejmowania:", liczba1 - liczba2)
    print("Wynik mnożenia:", liczba1 * liczba2)

    if liczba2 != 0:
        print("Wynik dzielenia:", liczba1 / liczba2)
    else:
        print("Nie można dzielić przez zero.")

    print()