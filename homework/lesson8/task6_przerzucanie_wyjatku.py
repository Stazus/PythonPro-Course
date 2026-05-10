"""
Program: Przerzucanie wyjątku z logowaniem

Opis działania:
- Funkcja próbuje pobrać wartość dla klucza 'wiek' ze słownika.
- Jesli klucz nie istnieje, loguje błąd i rzuca własny wyjętek.
- Główna część programu łap[ie wyjątek i informuje uzytkownika.
"""

import datetime # import modułu do pracy z datą i czasem

# Definicja własnego wyjatku
class BladPrzetwarzaniaDanychError(Exception):
    """Własny wyjatek zgłaszany, gdy brakuje wymaganego klucza w danych"""
    pass

def przetworz_dane(dane):
    """Funkcja próbuje odczytać wartość dla klucza 'wiek' ze słownika."""
    
    klucz = "wiek" # okreslamy, którego klucza szukamy w słowniku
    
    try:
        # Próba pobrania wartości ze słownika
        wartosc = dane[klucz] # jesli klucz nie istnieje, wywoła KeyError
        print(f"Wiek: {wartosc}") # jeśli klucz istnieje, wypisujemy jego wartość
        
    except KeyError as e: # blok przechwytuje błąd KeyError
        # Otwieramy plik log.txt w trybie dopisywania ('a')
        with open("log.txt", "a", encoding="utf-8") as log_file:
            # Pobieramy aktualną datę i czas w czytelnym formacie
            czas = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Zapisujemy do pliku informację o błędzie i czas jego wystapienia
            log_file.write(f"{czas} - KeyError: brak klucza {e}\n")
            # Rzucamy własny wyjatek z opisem, którego klucza brakowało
            raise BladPrzetwarzaniaDanychError(f"Brakuje klucza: {e}")
        
# --- Przykładowe użycie funkcji ---
try:
    dane_testowe = {"imie": "Jan"} # słownik bez klucza 'wiek'
    przetworz_dane(dane_testowe)
    
except BladPrzetwarzaniaDanychError as e: # przechwycenie własnego wyjatku
    # Informujemy użytkownika o błędzie przetwarzania danych
    print(f"Wystąpił błąd przetwarzania danych: {e}")