while True:
    # Pobranie pierwszej liczby lub zakończenie programu
    wejscie1 = input("Podaj pierwszą liczbę (lub 'koniec' aby zakończytć): ")
    if wejscie1.lower() == 'koniec':
        print("Koniec działania kalkulatora.")
        break
    
    #  Próba konwersji pierwszej liczby
    try:
        liczba1 = float(wejscie1)
    except ValueError:
        print("Błąd: pierwsza liczba nie jest prawidłowa.\n")
        continue
    
    # Pobieranie i walidacja drugiej liczby
    while True:
        wejscie2 = input("Podaj drugą liczbę: ")
        try:
            liczba2 = float(wejscie2)
            break
        except ValueError:
            print("Błąd: druga liczba nie jest prawidłowa. Spróbuj ponownie.")
            
    # Wybór działania matematycznego
    while True: 
        print("Wybierz działanie: + - * /")
        dzialanie = input("Wypisz symbol działania: ")
        
        if dzialanie == "+":
            print("Wynik dodawania: ", liczba1 + liczba2)
            break
        elif dzialanie == "-":
            print("Wynik odehmowania: ", liczba1 - liczba2)
            break
        elif dzialanie == "*":
            print("Wynik mnożenia: ", liczba1 * liczba2)
            break
        elif dzialanie == "/":
            if liczba2 != 0:
                print("Wynik dzielenia: ", liczba1 / liczba2)
            else:
                print("Błąd: nie można dzielić przez zero!")
            break
        else:
            print("Nieznane działanie. Użyj: +, -, *, lub /. Spróbuj ponownie.")
            
    # Pusta linia dla czytelności
    print()
    