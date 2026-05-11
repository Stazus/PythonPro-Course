# --- Wersja bez try...except ---
def pobierz_wartosc(slownik, klucz):
    """
    Funkcja bezpiecznie pobiera wartość dla danego klucza ze słownika.
    
    Działanie:
    1. Używa metody .get() słownika.
    2. Jeśli klucz istnieje, zwraca jego wartość.
    3. Jeśli klucza nie ma, zwraca None.
    """
    return slownik.get(klucz)  # .get() zwraca None, jeśli klucza nie ma


# --- Wersja z try...except ---
def pobierz_wartosc_try(slownik, klucz):
    """
    Funkcja próbuje pobrać wartość dla danego klucza ze słownika.
    
    Działanie:
    1. Próbuje pobrać wartość za pomocą slownik[klucz].
    2. Jeśli klucz istnieje, zwraca wartość.
    3. Jeśli klucz nie istnieje, wywołuje KeyError.
    4. Blok except łapie KeyError i zwraca None, dzięki czemu program nie przerywa działania.
    """
    try:
        return slownik[klucz]
    except KeyError:
        return None


# --- Przykładowe użycie ---
dane = {"imie": "Anna", "wiek": 25}

print("WERSJA .get():")
# Pobranie istniejącego klucza "imie" → zwróci "Anna"
print("Imię:", pobierz_wartosc(dane, "imie"))

# Pobranie nieistniejącego klucza "nazwisko" → zwróci None
print("Nazwisko:", pobierz_wartosc(dane, "nazwisko"))

print("\nWERSJA try...except:")
# Pobranie istniejącego klucza "wiek" → zwróci 25
print("Wiek:", pobierz_wartosc_try(dane, "wiek"))

# Pobranie nieistniejącego klucza "adres" → zwróci None, obsłużony wyjątek KeyError
print("Adres:", pobierz_wartosc_try(dane, "adres"))