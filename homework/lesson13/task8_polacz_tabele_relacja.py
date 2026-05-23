"""
Połączenie tabele (Relacja) i wyświetlenie przypisania w formie tabeli z tabulate

Skrypt tworzy w bazie uczelnia.db tabelę przypisania, która łączy studentów z audytoriami
(np. na egzamin). Następnie wstawia przykładowe przypisania i wyświetla wszystkie rekordy
w formie czytelnej tabeli w konsoli przy użyciu biblioteki tabulate.

Struktura tabeli przypisania:
- id_przypisania (INTEGER, PRIMARY KEY)
- id_studenta (INTEGER, FOREIGN KEY wskazujący na studenci.id_studenta)
- id_audytorium (INTEGER, FOREIGN KEY wskazujący na audytoria.id_audytorium)
"""

import sqlite3
from tabulate import tabulate

# Połączenie z bazą
conn = sqlite3.connect("uczelnia.db")
cursor = conn.cursor()

# Tworzenie tabeli przypisania z relacjami do studentów i audytoriów
cursor.execute("""
CREATE TABLE IF NOT EXISTS przypisania (
    id_przypisania INTEGER PRIMARY KEY,
    id_studenta INTEGER,
    id_audytorium INTEGER,
    FOREIGN KEY (id_studenta) REFERENCES studenci(id_studenta),
    FOREIGN KEY (id_audytorium) REFERENCES audytoria(id_audytorium)
)
""")

# Przykładowe przypisania (id_przypisania, id_studenta, id_audytorium)
przypisania = [
    (1, 1, 1),
    (2, 2, 2),
    (3, 3, 3),
    (4, 4, 1)
]

# Wstawianie przypisań do tabeli
cursor.executemany(
    "INSERT OR IGNORE INTO przypisania (id_przypisania, id_studenta, id_audytorium) VALUES (?, ?, ?)",
    przypisania
)

# Zatwierdzenie zmian
conn.commit()
print("Tabela 'przypisania' została utworzona i wypełniona przykładowymi danymi.\n")

# Pobranie danych z JOIN, aby wyświetlić studentów i audytoria
cursor.execute("""
SELECT p.id_przypisania,
       s.imie || ' ' || s.nazwisko AS student,
       a.nazwa_budynku || ' ' || a.numer_sali AS audytorium
FROM przypisania p
JOIN studenci s ON p.id_studenta = s.id_studenta
JOIN audytoria a ON p.id_audytorium = a.id_audytorium
""")

wyniki = cursor.fetchall()

# Wyświetlenie w formie tabeli przy użyciu tabulate
headers = ["ID Przypisania", "Student", "Audytorium"]
print(tabulate(wyniki, headers=headers, tablefmt="grid"))

# Zamknięcie połączenia
conn.close()