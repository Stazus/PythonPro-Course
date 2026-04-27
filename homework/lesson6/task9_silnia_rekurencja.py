def silnia(n: int) -> int:
    """
    Funkcja rekurencyjna oblicza silnię liczby n.
    
    Argumenty:
    n (int): liczba całowita, dla której obliczana jest silnia (n >= 0)
    
    Zwraca:
    int: silnia liczby n (n!)
    """
    if n == 0:
        return 1
    else:
        return n * silnia(n - 1)
    
    # Pobranie liczby od uzytkownika
try:
    liczba = int(input("Podaj liczbę całkowitą (n >= 0), dla której chcesz obliczyć silnię: "))
    if liczba < 0:
        print("Błąd: liczba nie może być ujemna.")
    else:
        wynik = silnia(liczba)
        print(f"Silnia z {liczba} wynosi {wynik}")
except ValueError:
    print("Błąd: należy podać liczbę całkowitą.")