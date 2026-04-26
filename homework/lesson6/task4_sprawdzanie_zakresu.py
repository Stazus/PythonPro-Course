# Zmienna globalna
POZIOM_DOSTEPU = "user"

# Funkcja próbująca zmienić zmienną bez użycia 'global'

def zmien_poziom():
    POZIOM_DOSTEPU = "admin"  # to jest nowa zmienna lokalna
    print("Wewnątrz funkcji: ", POZIOM_DOSTEPU)
    
# Wywołanie funkcji
zmien_poziom()

# Wartość zmiennej globalnej poza funkcją
print("Poza funkcją: ", POZIOM_DOSTEPU)