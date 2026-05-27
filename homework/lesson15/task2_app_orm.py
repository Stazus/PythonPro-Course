import database_orm as db


def pokaz_zadania():

    zadania = db.pobierz_zadania()

    if not zadania:
        print("Brak zadań na liście.")
        return

    print("\n--- Lista zadań ORM ---")

    for zadanie in zadania:

        status = "✓" if zadanie.zrobione else "✗"

        tagi = ", ".join(
            tag.nazwa for tag in zadanie.tagi
        ) or "brak"

        print(
            f"[{status}] ID: {zadanie.id}, "
            f"Opis: {zadanie.opis}, "
            f"Data utworzenia: {zadanie.data_utworzenia}, "
            f"Tagi: {tagi}"
        )

    print("----------------------\n")


def wyszukaj_zadania():

    fraza = input("Podaj frazę do wyszukania: ")

    zadania = db.wyszukaj_zadania(fraza)

    if not zadania:
        print("Nie znaleziono zadań.")
        return

    print("\n--- Wyniki wyszukiwania ORM ---")

    for zadanie in zadania:

        status = "✓" if zadanie.zrobione else "✗"

        print(
            f"[{status}] "
            f"ID: {zadanie.id}, "
            f"Opis: {zadanie.opis}, "
            f"Data utworzenia: {zadanie.data_utworzenia}"
        )

    print("------------------------------\n")


def main():

    db.init_db()

    while True:

        print("Menu ORM:")
        print("1. Pokaż zadania")
        print("2. Dodaj zadanie")
        print("3. Oznacz zadanie jako zrobione")
        print("4. Usuń zadanie")
        print("5. Wyjdź")
        print("6. Wyszukaj zadanie")
        print("7. Dodaj tag do zadania")

        wybor = input("Wybierz opcję: ")

        if wybor == '1':

            pokaz_zadania()

        elif wybor == '2':

            opis = input("Podaj opis zadania: ")

            db.dodaj_zadanie(opis)

            print("Zadanie dodane!")

        elif wybor == '3':

            try:
                id_zadania = int(
                    input("Podaj ID zadania: ")
                )

                db.oznacz_jako_zrobione(
                    id_zadania
                )

                print("Zadanie zaktualizowane!")

            except ValueError:

                print("Błędne ID.")

        elif wybor == '4':

            try:
                id_zadania = int(
                    input("Podaj ID zadania do usunięcia: ")
                )

                db.usun_zadanie(id_zadania)

                print("Zadanie usunięte!")

            except ValueError:

                print("Błędne ID.")

        elif wybor == '5':

            print("Do zobaczenia!")

            break

        elif wybor == '6':
            wyszukaj_zadania()
            
        elif wybor == '7':
            try:
                id_zadania = int(input("Podaj ID zadania: "))
                nazwa_tagu = input("Podaj nazwę taga: ")

                czy_dodano = db.dodaj_tag_do_zadania(id_zadania, nazwa_tagu)

                if czy_dodano:
                    print("Tag dodany do zadania!")
                else:
                    print("Nie znaleziono zadania o podanym ID.")

            except ValueError:
                print("Błędne ID.")
            

        else:

            print("Nieznana opcja.")


if __name__ == "__main__":
    main()