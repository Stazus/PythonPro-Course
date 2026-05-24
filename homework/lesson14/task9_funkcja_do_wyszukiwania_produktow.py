import sqlite3

def znajdz_produkty_w_kategorii(nazwa_kategorii):
    """
    Funkcja łączy się z bazą danych 'sklep.db' i zwraca listę produktów
    w podanej kategorii.

    Argument:
    - nazwa_kategorii (str): nazwa kategorii, np. 'Elektronika'

    Zwraca:
    - lista krotek (nazwa_produktu, cena) dla wszystkich produktów w kategorii
    """
    produkty = []
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.nazwa_produktu, p.cena
            FROM Produkty AS p
            JOIN Kategorie AS k ON p.id_kategorii = k.id_kategorii
            WHERE k.nazwa_kategorii = ?
            ORDER BY p.nazwa_produktu
        """, (nazwa_kategorii,))

        produkty = cursor.fetchall()

    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych:", e)

    finally:
        conn.close()

    return produkty


if __name__ == "__main__":
    # Przykładowe wywołanie funkcji
    kategoria = 'Elektronika'
    wyniki = znajdz_produkty_w_kategorii(kategoria)
    
    if wyniki:
        print(f"Produkty w kategorii '{kategoria}':\n")
        for nazwa, cena in wyniki:
            print(f"- {nazwa}: {cena:.2f} zł")
    else:
        print(f"Brak produktów w kategorii '{kategoria}'.")