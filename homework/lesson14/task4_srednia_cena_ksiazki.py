import sqlite3

def srednia_cena_ksiazek():
    """
    Łączy się z bazą danych 'sklep.db' i oblicza średnią cenę
    produktów z kategorii 'Książki'.
    
    W zapytaniu SQL używana jest funkcja AVG() oraz klauzula JOIN,
    aby połączyć tabele Produkty i Kategorie po id_kategorii.
    """
    try:
        # Połączenie z bazą danych
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        # Zapytanie SQL z AVG() i JOIN
        cursor.execute("""
            SELECT AVG(p.cena) AS srednia_cena
            FROM Produkty AS p
            JOIN Kategorie AS k ON p.id_kategorii = k.id_kategorii
            WHERE k.nazwa_kategorii = 'Książki'
        """)

        wynik = cursor.fetchone()

        if wynik and wynik[0] is not None:
            print(f"Średnia cena produktów z kategorii 'Książki': {wynik[0]:.2f} zł")
        else:
            print("Brak produktów w kategorii 'Książki'.")

    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    srednia_cena_ksiazek()