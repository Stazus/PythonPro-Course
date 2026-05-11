"""
Program: Automatyczne testowanie wyjątków FileNotFoundError i PermissionError

Opis działania i sposób testowania:
1. Uruchom program w terminalu:
       python3 czytanie_pliku.py

2. Po uruchomieniu program zapyta, który test chcesz wykonać:
   - Wpisz 1 → test FileNotFoundError (plik nie istnieje)
   - Wpisz 2 → test PermissionError (plik istnieje, ale brak uprawnień do odczytu)
   - Wpisz 3 → test normalnego odczytu (plik istnieje i ma prawa odczytu)

3. Po teście PermissionError program automatycznie przywróci uprawnienia pliku.
"""

import os  # moduł do pracy z plikami i prawami dostępu w systemie

def czytaj_plik(nazwa_pliku):
    """
    Funkcja próbuje otworzyć i odczytać plik o podanej nazwie.
    Obsługuje wyjątki:
    - FileNotFoundError → plik nie istnieje
    - PermissionError → brak uprawnień do odczytu
    - Inne nieoczekiwane wyjątki
    """
    try:
        # Otwieramy plik w trybie odczytu (r) z kodowaniem UTF-8
        with open(nazwa_pliku, "r", encoding="utf-8") as plik:
            zawartosc = plik.read()  # odczyt całej zawartości pliku
            print("\nZawartość pliku:\n")
            print(zawartosc)

    except FileNotFoundError:
        # Wyjątek, gdy plik nie istnieje
        print(f"Błąd: Plik '{nazwa_pliku}' nie istnieje.")

    except PermissionError:
        # Wyjątek, gdy brak uprawnień do odczytu
        print(f"Błąd: Brak uprawnień do odczytu pliku '{nazwa_pliku}'.")

    except Exception as e:
        # Obsługa innych, nieoczekiwanych błędów
        print(f"Wystąpił nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    # Tworzymy plik testowy z normalnym dostępem
    plik_dostepny = "test_normalny.txt"
    with open(plik_dostepny, "w", encoding="utf-8") as f:
        f.write("To jest plik testowy z normalnym dostępem.")

    # Tworzymy plik testowy, który posłuży do testu PermissionError
    plik_zablokowany = "test_brak_uprawnien.txt"

    # Jeśli plik już istnieje, przywracamy prawa do zapisu (0o644), żeby można go było nadpisać
    if os.path.exists(plik_zablokowany):
        os.chmod(plik_zablokowany, 0o644)

    # Tworzymy plik i zapisujemy w nim tekst
    with open(plik_zablokowany, "w", encoding="utf-8") as f:
        f.write("To jest plik, do którego zablokujemy dostęp.")

    # Blokujemy dostęp do pliku (0o000 → brak praw do odczytu, zapisu i wykonania)
    os.chmod(plik_zablokowany, 0o000)

    # Wyświetlamy menu wyboru testu
    print("Wybierz test:")
    print("1 - Plik nie istnieje")
    print("2 - Brak uprawnień do odczytu")
    print("3 - Normalny odczyt pliku")

    wybor = input("Podaj numer testu: ")

    if wybor == "1":
        # Test odczytu pliku, który nie istnieje → FileNotFoundError
        czytaj_plik("plik_ktorego_nie_ma.txt")
    elif wybor == "2":
        # Test odczytu pliku bez uprawnień → PermissionError
        czytaj_plik(plik_zablokowany)
        # Przywracamy prawa po teście, żeby plik dało się potem usunąć
        os.chmod(plik_zablokowany, 0o644)
    elif wybor == "3":
        # Normalny odczyt istniejącego pliku
        czytaj_plik(plik_dostepny)
    else:
        print("Nieznana opcja testu.")