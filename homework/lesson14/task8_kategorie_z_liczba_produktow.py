import sqlite3

def liczba_produktow_w_kategoriach():
    """
    Łączy się z bazą danych 'sklep.db' i wyświetla dla każdej kategorii:
    - nazwę kategorii,
    - liczbę produktów w tej kategorii.
    
    W zapytaniu SQL używane są:
    - JOIN do połączenia tabel Kategorie i Produkty,
    - COUNT() do zliczenia produktów,
    - GROUP BY do pogrupowania wyników według kategorii.
    """
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        # Zapytanie SQL z COUNT(), JOIN i GROUP BY
        cursor.execute("""
            SELECT k.nazwa_kategorii, COUNT(p.id_produktu) AS liczba_produktow
            FROM Kategorie AS k
            LEFT JOIN Produkty AS p ON k.id_kategorii = p.id_kategorii
            GROUP BY k.id_kategorii, k.nazwa_kategorii
        """)

        wyniki = cursor.fetchall()

        if wyniki:
            print("Kategorie i liczba produktów w każdej kategorii:\n")
            for nazwa, liczba in wyniki:
                print(f"{nazwa}: {liczba} produktów")
        else:
            print("Brak kategorii lub produktów w bazie.")

    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    liczba_produktow_w_kategoriach()