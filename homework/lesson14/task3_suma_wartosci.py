import sqlite3

def suma_wartosci_elektroniki():
    """
    Łączy się z bazą danych 'sklep.db' i oblicza łączną wartość
    wszystkich produktów należących do kategorii 'Elektronika'.
    
    W zapytaniu używana jest funkcja SUM() oraz klauzula JOIN,
    łącząca tabele Produkty i Kategorie po id_kategorii.
    """
    try:
        # Połączenie z bazą danych
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        # Zapytanie SQL z SUM() i JOIN
        cursor.execute("""
            SELECT SUM(p.cena) AS laczna_wartosc
            FROM Produkty AS p
            JOIN Kategorie AS k ON p.id_kategorii = k.id_kategorii
            WHERE k.nazwa_kategorii = 'Elektronika'
        """)

        wynik = cursor.fetchone()

        if wynik and wynik[0] is not None:
            print(f"Łączna wartość produktów z kategorii 'Elektronika': {wynik[0]:.2f} zł")
        else:
            print("Brak produktów w kategorii 'Elektronika'.")

    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    suma_wartosci_elektroniki()