import sqlite3

def wyswietl_klientow():
    """
    Łączy się z bazą danych 'sklep.db' i wyświetla listę wszystkich klientów.
    
    Skrypt pobiera z tabeli Klienci kolumny:
    - imię klienta,
    - adres e-mail.
    """
    try:
        # Połączenie z bazą danych
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        # Zapytanie SQL pobierające dane klientów
        cursor.execute("SELECT imie, email FROM Klienci")

        wyniki = cursor.fetchall()

        if wyniki:
            print("Lista klientów:\n")
            for imie, email in wyniki:
                print(f"Imię: {imie}, Email: {email}")
        else:
            print("Brak klientów w bazie danych.")

    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    wyswietl_klientow()