def loguj(funkcja):
    def opakowanie(*args, **kwargs):
        print(f"Uruchamiam funkcję {funkcja.__name__}...") # Przed wywołaniem
        wynik = funkcja(*args, **kwargs)                   # Wywołanie funkcji
        print(f"Zakończono funkcję {funkcja.__name__}")    # Po zakońceniu
        return wynik
    return opakowanie

# Przykład użycia dekoratora
@loguj
def przywitaj(imie):
    print(f"Cześć, {imie}!")
    
# Wywołanie udekorowanej funkcji
przywitaj("Anna")