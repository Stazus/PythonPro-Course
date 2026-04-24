kursy = {"USD": 4.0, "EUR": 4.3}

print("Prosty kalkulator walut (PLN -> USD/EUR)")

while True:
    try:
        pln = float(input("Podaj kwotę w PLN: "))
        
        waluta = input("Na jaką walutę chcesz wymienić? (USD/EUR):").strip().upper()
        
        # Przeliczanie na wybraną walutę
        if waluta == "USD":
            wynik = pln / kursy["USD"]
            print(f"{pln} PLN = {wynik:.2f} USD")
        elif waluta == "EUR":
            wynik = pln / kursy["EUR"]
            print(f"{pln} PLN = {wynik:.2f} EUR")
        else:
            print("Błąd: Nieobsługiwana waluta. Wybierz USD lub EUR.")
            continue # wraca na początek pętli
        
        # Czy kontynuować?
        kontynuuj = input("Czy chcesz kontynuować? (tak/nie): ").strip().lower()
        if kontynuuj == "nie":
            print("Dziękujemy za skorzystanie z kalkulatora.")
            break
        
    except ValueError:
        print("Błąd: Podaj poprawną liczbę jako kwotę.")