import sqlite3

def zamowienia_anny_nowak():
    """
    Łączy się z bazą danych 'sklep.db' i wyświetla nazwy produktów,
    które zostały zamówione przez klienta 'Anna Nowak'.
    
    W zapytaniu SQL używany jest JOIN, aby połączyć cztery tabele:
    Klienci, Zamowienia, Zamowienia_Produkty i Produkty.
    """
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        # Zapytanie SQL łączące cztery tabele
        cursor.execute("""
            SELECT p.nazwa_produktu
            FROM Klienci AS k
            JOIN Zamowienia AS z ON k.id_klienta = z.id_klienta
            JOIN Zamowienia_Produkty AS zp ON z.id_zamowienia = zp.id_zamowienia
            JOIN Produkty AS p ON zp.id_produktu = p.id_produktu
            WHERE k.imie = 'Anna Nowak'
        """)

        wyniki = cursor.fetchall()

        if wyniki:
            print("Produkty zamówione przez Annę Nowak:\n")
            for (produkt,) in wyniki:
                print(f"- {produkt}")
        else:
            print("Anna Nowak nie złożyła żadnych zamówień.")

    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    zamowienia_anny_nowak()