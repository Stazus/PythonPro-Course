class InvalidPasswordError(Exception):
    """Wyjatek zgłaszany przy niepoprawnym hasle."""
    pass

def ustaw_haslo(haslo):
    """Sprawdza, czy hasło ma co najmniej 8 znaków. Jeśli nie, rzuca wyjątek."""
    if len(haslo) < 8:
        raise InvalidPasswordError("Hasło musi mieć co najmniej 8 znaków!")
    print("Hasło ustawione poprawnie.")
    
# Interaktywny test
haslo = input("Podaj hasło do ustawienia: ")

try:
    ustaw_haslo(haslo)
except InvalidPasswordError as e:
    print(f"Błąd: {e}")