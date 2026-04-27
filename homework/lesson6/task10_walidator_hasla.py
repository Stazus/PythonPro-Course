def sprawdz_haslo(haslo: str) -> bool:
    """
    Funkcja sprawdza czy podane haslo spełnia podstawowe wymagania bezpieczeństwa.
    
    Wymagania:
    - Ma co najmniej 8 znaków
    - Zawiera co najmniej jedna wielka literę (A-Z)
    - Zawiera co najmniej jedną cyfrę (0-9)
    
    Argumenty:
    haslo (str): Hasło do sprawdzenia
    
    Zwraca:
    bool: True, jesli hasło spełnia wszystkie warunki, False w przeciwnym razie
    """
    
    # Sprawdzenie długości hasła
    if len(haslo) < 8:
        return False
    
    # Spradzenie obecności przynajmniej jednej wielkiej litery
    if not any(c.isupper() for c in haslo):
        return False
    
    # Sprawzenie obecności przynajmniej jednej cyfry
    if not any(c.isdigit() for c in haslo):
        return False
    
    # Jeśli wszystkie warunki są spełnione, hasło jest poprawne
    return True

# --- Główna część programu ---
# Pobranie hasła od użytkownika
uzytkownik_haslo = input("Podaj hasło do sprawzenia: ")

# Sprawdzenie hasła i wypisanie wyniku
if sprawdz_haslo(uzytkownik_haslo):
    print("Hasło jest poprawne.")
else:
    print("Hasło nie spełnia wymagań.")
    
    