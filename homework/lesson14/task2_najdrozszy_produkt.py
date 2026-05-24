import sqlite3

def znajdz_najdrozszy_produkt():
    """
    Łączy się z bazą danych 'sklep.db" i wyszukuje najdroższy
    produkt w tabeli 'Produkty przy uzyciu funkcji SQL MAX().
    Wyświetla jego nazwę i cenę.
    """
    try:
        # Nawiązanie połączenia z bazą danych
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()
        
        # Zapytanie SQL z funkcją MAX()
        cursor.execute("""
            SELECT nazwa_produktu, cena
            FROM Produkty
            WHERE cena = (SELECT MAX(cena) FROM Produkty)                       
        """)
        
        wynik = cursor.fetchone()
        
        if wynik:
            nazwa, cena = wynik
            print(f"Najdroższy produkt: {nazwa} ({cena:.2f} zł)")
        else:
            print("Brak produktów w bazie danych.")
            
    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych: ", e)
        
    finally:
        conn.close()
        
if __name__ == "__main__":
    znajdz_najdrozszy_produkt()