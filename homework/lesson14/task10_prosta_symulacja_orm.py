import sqlite3

class Produkt:
    """
    Klasa reprezentująca produkt w sklepie.

    Atrybuty:
    - id_produktu (int): unikalny identyfikator produktu
    - nazwa_produktu (str): nazwa produktu
    - cena (float): cena produktu
    """
    def __init__(self, id_produktu, nazwa_produktu, cena):
        self.id_produktu = id_produktu
        self.nazwa_produktu = nazwa_produktu
        self.cena = cena

    def __repr__(self):
        return f"Produkt(id={self.id_produktu}, nazwa='{self.nazwa_produktu}', cena={self.cena:.2f} zł)"


def pobierz_wszystkie_produkty():
    """
    Łączy się z bazą danych 'sklep.db', pobiera wszystkie produkty
    z tabeli Produkty i zwraca listę obiektów klasy Produkt.
    """
    produkty = []
    try:
        conn = sqlite3.connect('sklep.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id_produktu, nazwa_produktu, cena FROM Produkty")
        wiersze = cursor.fetchall()

        for wiersz in wiersze:
            produkt = Produkt(*wiersz)
            produkty.append(produkt)

    except sqlite3.Error as e:
        print("Błąd podczas pracy z bazą danych:", e)

    finally:
        conn.close()

    return produkty


if __name__ == "__main__":
    lista_produktow = pobierz_wszystkie_produkty()
    print("Lista wszystkich produktów:\n")
    for produkt in lista_produktow:
        print(produkt)