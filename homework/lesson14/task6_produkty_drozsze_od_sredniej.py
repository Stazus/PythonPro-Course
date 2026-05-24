import sqlite3

def produkty_drozsze_od_sredniej():
    """
    Łączy się z bazą danych 'sklep.db' i wyświetla produkty,
    których cena jest wyższa niż średnia cena wszystkich produktów.
    """
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nazwa_produktu, cena 
            FROM Produkty
            WHERE cena > (SELECT AVG(cena) FROM Produkty)
            ORDER BY cena DESC
        """)

        wyniki = cursor.fetchall()

        if wyniki:
            print("Produkty droższe od średniej ceny:\n")
            for nazwa, cena in wyniki:
                print(f"Nazwa: {nazwa}, Cena: {cena:.2f} zł")
        else:
            print("Brak produktów droższych od średniej ceny.")

    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    produkty_drozsze_od_sredniej()