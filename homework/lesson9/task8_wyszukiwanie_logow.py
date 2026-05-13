"""
Program: Wyszukiwarka logów
Opis:
    Ten program przeszukuje plik logów (log.txt) w poszukiwaniu określonego słowa 
    podanego przez użytkownika (np. "ERROR").
    Wszystkie linie zawierające to słowo są zapisywane do nowego pliku 
    wyniki_wyszukiwania.txt.
"""

def main():
    slowo = input("Podaj słowo do wyszukania w logach: ")

    try:
        with open("log.txt", "r", encoding="utf-8") as log_file:
            with open("wyniki_wyszukiwania.txt", "w", encoding="utf-8") as wynik_file:
                for linia in log_file:
                    if slowo in linia:
                        wynik_file.write(linia)
        print("Wyszukiwanie zakończone. Sprawdź plik wyniki_wyszukiwania.txt")
    except FileNotFoundError:
        print("Błąd: Plik log.txt nie istnieje w bieżącym katalogu.")

if __name__ == "__main__":
    main()