def sumuj_liczby_z_pliku():
    """
    Program:
    - pyta użytkownika o nazwę pliku - należy podac nazwę pliku: 
    task10_sumator_liczb_z_pliku.py utworzonego dla potrzeb tego zadania,
    - odczytuje plik linia po linii,
    - próbuje zamieniać linie na liczby,
    - sumuje poprawne liczby,
    - ignoruje błędne linie (ValueError),
    - obsługuje brak pliku (FileNotFoundError),
    - zawsze wyświetla sumę w bloku finally.
    """

    suma = 0

    try:
        # a. Pobranie nazwy pliku od użytkownika
        nazwa = input("Podaj nazwę pliku: ")

        # b. Otwieramy plik w trybie odczytu
        # with automatycznie zamknie plik po zakończeniu pracy
        with open(nazwa, "r", encoding="utf-8") as plik:

            # c. Czytamy plik linia po linii
            for linia in plik:

                # strip() usuwa spacje i znak nowej linii \n
                linia = linia.strip()

                # Pomijamy puste linie
                if not linia:
                    continue

                try:
                    # d. Próba zamiany tekstu na liczbę
                    liczba = float(linia)

                    # Dodajemy liczbę do sumy
                    suma += liczba

                except ValueError:
                    # Jeśli konwersja się nie udała
                    print(f"Ignoruję niepoprawną linię: '{linia}'")

    except FileNotFoundError:
        # e. Obsługa sytuacji, gdy plik nie istnieje
        print("Błąd: Plik nie istnieje!")

    finally:
        # finally wykona się zawsze: czy był błąd czy nie
        print(f"Suma liczb: {suma}")


# ============================
# Uruchomienie programu
# __name__ to specjalna zmienna tworzona automatycznie przez Pythona.
# Jeśli plik jest uruchamiany bezpośrednio, Python ustawia:
# __name__ = "__main__"
#
# Dzięki temu poniższy warunek jest spełniony i program uruchamia funkcję.
#
# Jeśli jednak ten plik zostanie zaimportowany do innego pliku jako moduł,
# kod wewnątrz tego warunku nie wykona się automatycznie.
# ============================
if __name__ == "__main__":
    sumuj_liczby_z_pliku()