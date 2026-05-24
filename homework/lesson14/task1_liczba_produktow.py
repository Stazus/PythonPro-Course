import sqlite3

def policz_produkty():
    """
    Łączy się z bazą danych 'sklep.db' i zlicza,
    ile produktów znajduje się w tabeli 'Produkty'.
    Wykorzystuje funkcję SQL COUNT().
    """
    try:
        # Nawiązanie połączenia z bazą
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        # Zapytanie SQL z funkcją COUNT()
        cursor.execute("SELECT COUNT(*) FROM Produkty")
        wynik = cursor.fetchone()[0]

        # Wyświetlenie wyniku
        print(f"Liczba produktów w tabeli 'Produkty': {wynik}")

    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych:", e)

    finally:
        # Zamknięcie połączenia
        conn.close()


if __name__ == "__main__":
    policz_produkty()