import sqlite3

DATABASE_NAME = "todo_raw_class.db"


class TaskManagerRaw:
    """Klasa do zarządzania zadaniami w bazie SQLite przy użyciu Raw SQL."""

    def __init__(self):
        """Konstruktor inicjalizuje bazę danych."""
        self.init_db()

    def init_db(self):
        """Tworzy tabelę zadania, jeśli nie istnieje."""

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS zadania (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opis TEXT NOT NULL,
                zrobione BOOLEAN NOT NULL CHECK (zrobione IN (0, 1)),
                priorytet INTEGER DEFAULT 1
            )
            """)

            conn.commit()

    def dodaj_zadanie(self, opis: str, priorytet: int):
        """Dodaje nowe zadanie."""

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO zadania (opis, zrobione, priorytet)
                VALUES (?, ?, ?)
                """,
                (opis, False, priorytet)
            )

            conn.commit()

    def pobierz_zadania(self):
        """Pobiera wszystkie zadania."""

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, opis, zrobione, priorytet FROM zadania"
            )

            return cursor.fetchall()

    def oznacz_jako_zrobione(self, id_zadania: int):
        """Oznacza zadanie jako zrobione."""

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE zadania SET zrobione = ? WHERE id = ?",
                (True, id_zadania)
            )

            conn.commit()

    def usun_zadanie(self, id_zadania: int):
        """Usuwa zadanie po ID."""

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM zadania WHERE id = ?",
                (id_zadania,)
            )

            conn.commit()
            
    def edytuj_zadanie(self, id_zadania: int, nowy_opis: str):
        """Edytuje opis zadania o podanym ID."""

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE zadania SET opis = ? WHERE id = ?",
                (nowy_opis, id_zadania)
            )

            conn.commit()
            

    def wyszukaj_zadania(self, fraza: str):
        """Wyszukuje zadania po fragmencie opisu."""

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, opis, zrobione, priorytet
                FROM zadania
                WHERE opis LIKE ?
                """,
                (f"%{fraza}%",)
            )

            return cursor.fetchall()


def pokaz_zadania(manager: TaskManagerRaw):
    """Wyświetla wszystkie zadania."""

    zadania = manager.pobierz_zadania()

    if not zadania:
        print("Brak zadań na liście.")
        return

    print("\n--- Lista zadań RAW SQL - klasy ---")

    for zadanie in zadania:
        status = "✓" if zadanie[2] else "✗"

        print(
            f"[{status}] "
            f"ID: {zadanie[0]}, "
            f"Opis: {zadanie[1]}, "
            f"Priorytet: {zadanie[3]}"
        )

    print("----------------------------------\n")


def pokaz_wyniki_wyszukiwania(manager: TaskManagerRaw):
    """Wyświetla zadania znalezione po frazie."""

    fraza = input("Podaj frazę do wyszukania: ")

    zadania = manager.wyszukaj_zadania(fraza)

    if not zadania:
        print("Nie znaleziono zadań.")
        return

    print("\n--- Wyniki wyszukiwania RAW SQL - klasy ---")

    for zadanie in zadania:
        status = "✓" if zadanie[2] else "✗"

        print(
            f"[{status}] "
            f"ID: {zadanie[0]}, "
            f"Opis: {zadanie[1]}, "
            f"Priorytet: {zadanie[3]}"
        )

    print("-----------------------------------------\n")


def main():
    manager = TaskManagerRaw()

    while True:
        print("Menu RAW SQL - klasy:")        
        print("1. Pokaż zadania")
        print("2. Dodaj zadanie")
        print("3. Oznacz zadanie jako zrobione")
        print("4. Usuń zadanie")
        print("5. Wyszukaj zadanie")
        print("6. Edytuj zadanie")
        print("7. Wyjdź")
        

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            pokaz_zadania(manager)

        elif wybor == "2":
            opis = input("Podaj opis zadania: ")

            try:
                priorytet = int(input("Podaj priorytet zadania (1-5): "))
                manager.dodaj_zadanie(opis, priorytet)
                print("Zadanie dodane!")

            except ValueError:
                print("Priorytet musi być liczbą.")

        elif wybor == "3":
            try:
                id_zadania = int(input("Podaj ID zadania do oznaczenia: "))
                manager.oznacz_jako_zrobione(id_zadania)
                print("Zadanie zaktualizowane!")

            except ValueError:
                print("Błędne ID. Podaj liczbę.")

        elif wybor == "4":
            try:
                id_zadania = int(input("Podaj ID zadania do usunięcia: "))
                manager.usun_zadanie(id_zadania)
                print("Zadanie usunięte!")

            except ValueError:
                print("Błędne ID. Podaj liczbę.")

        elif wybor == "5":
            pokaz_wyniki_wyszukiwania(manager)
            
        elif wybor == "6":
            try:
                id_zadania = int(input("Podaj ID zadania do edycji: "))
                nowy_opis = input("Podaj nowy opis zadania: ")

                manager.edytuj_zadanie(id_zadania, nowy_opis)

                print("Zadanie zaktualizowane!")

            except ValueError:
                print("Błędne ID. Podaj liczbę.")
            

        elif wybor == "7":
            print("Do zobaczenia!")
            break

        else:
            print("Nieznana opcja, spróbuj ponownie.")


if __name__ == "__main__":
    main()