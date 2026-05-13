"""
Program: Odczyt konfiguracji z pliku JSON

Opis działania:
1. Program otwiera plik 'config.json', w którym zapisane są ustawienia aplikacji.
2. Wczytuje zawartość pliku jako słownik Pythona.
3. Odczytuje z niego wartości: 'uzytkownik' oraz 'motyw'.
4. Wyświetla spersonalizowany komunikat powitalny.
5. Obsługuje sytuacje, gdy plik nie istnieje lub zawiera błędny JSON.
"""

import json  # moduł do obsługi JSON

# nazwa pliku z konfiguracją
plik = "config.json"

try:
    # otwarcie pliku w trybie odczytu z kodowaniem UTF-8
    with open(plik, "r", encoding="utf-8") as f:
        konfiguracja = json.load(f)  # wczytanie zawartości pliku do słownika

    # odczyt wartości z wczytanego słownika
    uzytkownik = konfiguracja.get("uzytkownik", "nieznany")  # jeśli brak klucza, użyj "nieznany"
    motyw = konfiguracja.get("motyw", "domyślny")            # jeśli brak klucza, użyj "domyślny"

    # wyświetlenie komunikatu powitalnego
    print(f"Witaj, {uzytkownik}! Twój motyw to {motyw}.")

except FileNotFoundError:
    # sytuacja, gdy plik nie istnieje
    print(f"Plik {plik} nie został znaleziony.")
except json.JSONDecodeError:
    # sytuacja, gdy plik istnieje, ale nie jest poprawnym JSON-em
    print(f"Plik {plik} zawiera niepoprawny format JSON.")