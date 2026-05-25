import database_raw as db


def pokaz_zadania():
    """Wyświetla listę wszystkich zadań."""
    
    zadania = db.pobierz_zadania()

    if not zadania:
        print("Brak zadań na liście.")
        return

    print("\n--- Twoja lista zadań ---")

    for zadanie in zadania:
        status = "✓" if zadanie[2] else "✗"

        print(f"[{status}] ID: {zadanie[0]}, Opis: {zadanie[1]}")

    print("------------------------\n")


def main():

    # Inicjalizacja bazy danych
    db.init_db()

    while True:

        print("Menu:")    
        print("1. Pokaż zadania")
        print("2. Dodaj zadanie")
        print("3. Oznacz zadanie jako zrobione")
        print("4. Usuń zadanie")
        print("5. Wyjdź")

        wybor = input("Wybierz opcję: ")

        # Pokazanie wszystkich zadań
        if wybor == '1':
            pokaz_zadania()

        # Dodawanie zadania
        elif wybor == '2':

            opis = input("Podaj opis zadania: ")

            db.dodaj_zadanie(opis)

            print("Zadanie dodane!")

        # Oznaczenie zadania jako zrobione
        elif wybor == '3':

            try:
                id_zadania = int(
                    input("Podaj ID zadania do oznaczenia: ")
                )

                db.oznacz_jako_zrobione(id_zadania)

                print("Zadanie zaktualizowane!")

            except ValueError:
                print("Błędne ID. Podaj liczbę.")

        # Wyjście z programu            
        elif wybor == '4':
            try:
                id_zadania = int(input("Podaj ID zadania do usunięcia: "))
                db.usun_zadanie(id_zadania)
                print("Zadanie usunięte!")

            except ValueError:
                print("Błędne ID. Podaj liczbę.")

        elif wybor == '5':
            print("Do zobaczenia!")
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")


if __name__ == "__main__":
    main()