"""
Funkcja wyszukująca salę studenta

Skrypt definiuje funkcję znajdz_sale_studenta(nazwisko), która przyjmuje nazwisko studenta
jako argument. Funkcja łączy się z bazą uczelnia.db, wykonuje JOIN między tabelami 
studenci, przypisania i audytoria, a następnie wyświetla informację, w jakim budynku i
w jakiej sali znajduje się dany student. Wynik jest wyświetlany w formie tabeli przy użyciu tabulate.
"""

import sqlite3
from tabulate import tabulate

def znajdz_sale_studenta(nazwisko):
    """Znajduje salę i budynek dla studenta o podanym nazwisku."""
    conn = sqlite3.connect("uczelnia.db")
    cursor = conn.cursor()

    # Zapytanie z JOIN
    cursor.execute("""
    SELECT s.imie || ' ' || s.nazwisko AS student,
           a.nazwa_budynku || ' ' || a.numer_sali AS audytorium
    FROM studenci s
    JOIN przypisania p ON s.id_studenta = p.id_studenta
    JOIN audytoria a ON p.id_audytorium = a.id_audytorium
    WHERE s.nazwisko = ?
    """, (nazwisko,))

    wyniki = cursor.fetchall()
    
    if wyniki:
        headers = ["Student", "Audytorium"]
        print(tabulate(wyniki, headers=headers, tablefmt="grid"))
    else:
        print(f"Nie znaleziono studenta o nazwisku '{nazwisko}'.")

    conn.close()


# Przykład użycia funkcji
if __name__ == "__main__":
    nazwisko = input("Podaj nazwisko studenta, którego salę chcesz znaleźć: ")
    znajdz_sale_studenta(nazwisko)