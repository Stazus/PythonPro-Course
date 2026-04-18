def oblicz_pole_prostokata(a, b):
    """
    Funkcja oblicza pole prostokąta na podstawie długości boków a i b.
    Zwraca wynik jako liczbę całkowitą lub zmiennoprzecinkową.
    """
    
    # Mnożenie długości boków w celu uzyskania pola
    pole = a * b
    
    # Zwrócenie obliczonego pola
    return pole

# Przypisanie długości boków prostokąta
bok_a = 10
bok_b = 20

# Wywołanie funkcji i zapisanie wyniku do zmiennej
wynik = oblicz_pole_prostokata(bok_a, bok_b)

# Wyświetlenie wyniku na ekranie w formacie tekstowym
print(f"Pole prostokąta o bokach {bok_a} i {bok_b} wynosi {wynik}.")