"""
Program: Licznik słów w pliku
Opis: Program pyta użytkownika o nazwę pliku tekstowego, odczytuje jego zawartość,
      a następnie zlicza i wyświetla całkowitą liczbę słów w pliku. 
      Obsługuje sytuację, gdy podany plik nie istnieje.
"""

def licznik_slow():
    # Pytamy użytkownika o nazwę pliku
    nazwa_pliku = input("Podaj nazwę pliku: ") # można podać nazwę pliku utworzonego w poprzednim zadaniu - dziennik.txt

    try:
        # Otwieramy plik w trybie odczytu z kodowaniem UTF-8
        with open(nazwa_pliku, "r", encoding="utf-8") as plik:
            tekst = plik.read()  # Odczytujemy całą zawartość pliku
    except FileNotFoundError:
        # Obsługa błędu, gdy plik nie istnieje
        print(f"Błąd: plik '{nazwa_pliku}' nie istnieje.")
        return  # Kończymy działanie programu

    # Dzielimy tekst na słowa według białych znaków (spacje, tabulatory, znaki nowej linii)
    slowa = tekst.split()

    # Zliczamy liczbę słów
    liczba_slow = len(slowa)

    # Wyświetlamy wynik
    print(f"Całkowita liczba słów w pliku '{nazwa_pliku}' wynosi: {liczba_slow}")

# Uruchamiamy funkcję
if __name__ == "__main__":
    licznik_slow()