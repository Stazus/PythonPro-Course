# Definicja własnego wyjątku
class BladWalidacjiError(Exception):
    def __init__(self, lista_bledow):
        """
        lista_bledow - lista komunikatów o błędach (str)
        """
        self.lista_bledow = lista_bledow
        # Łączymy wzystkie błędy w jeden czytelny komunikat
        super().__init__(";".join(lista_bledow))
        
def waliduj_haslo(haslo):
    """
    Funkcja sprawdza poprawność hasła.
    Zwraca listę błędów walidacji.
    Jeśli lista nie jest pusta -> rzuca wyjątek BladWalidacjiError.
    
    Kryteria.
    1. Minimum 8 znaków
    2. Przynajmniej 1 wielka litera
    3. Przynajmniej 1 cyfra
    4. Przynajmniej 1 znak specjalny
    """
    bledy = []
    
    if len(haslo) < 8:
        bledy.append("Hasło musi mieć co najmniej 8 znaków")
        
    if not any(ch.isupper() for ch in haslo):
        bledy.append("Hasło musi zawierać wielką literę")
        
    if not any(ch.isdigit() for ch in haslo):
        bledy.append("Hasło musi zawierać cyfrę")
        
    if not any(not ch.isalnum() for ch in haslo):
        bledy.append("Hasło musi zawieraać znak specjalny")
        
    if bledy:
        raise BladWalidacjiError(bledy)
    
    return True # jesli nie ma błędów, hasło jest poprawne

# --- Przykładowe użycie ---
hasla_testowe = [
    "abc",          # za krótkie
    "abcdefgh",     # brak dużej litery, cyfry i znaku specjalnego
    "Abcdefgh",     # brak cyfry i znaku specjalnego
    "Abcdefg1",     # brak znaku specjalnego
    "Abcdefg1!"     # poprawne
]

for h in hasla_testowe:
    print(f"Test hasła: {h}")
    try:
        waliduj_haslo(h)
        print("Hasło poprawne\n")
    except BladWalidacjiError as e:
        print("Błędy: ", e.lista_bledow, "\n")