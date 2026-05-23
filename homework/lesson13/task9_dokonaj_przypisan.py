"""
Przypisanie studentów do audytoriów

Skrypt pobiera wszystkich studentów i audytoria z bazy uczelnia.db, a następnie przypisuje
każdego studenta do jednego audytorium. Przypisania są wstawiane do tabeli przypisania,
a następnie wyświetlane w formie czytelnej tabeli przy użyciu biblioteki tabulate.
"""

import sqlite3
from tabulate import tabulate

# Połączenie z bazą
conn = sqlite3.connect("uczelnia.db")
cursor = conn.cursor()

# Pobranie wszystkich studentów
cursor.execute("SELECT id_studenta, imie, nazwisko FROM studenci")
studenci = cursor.fetchall()

# Pobranie wszystkich audytoriów
cursor.execute("SELECT id_audytorium, nazwa_budynku, numer_sali FROM audytoria")
audytoria = cursor.fetchall()

# Dokonanie przypisań (cyklicznie student -> audytorium)
przypisania = []
for i, student in enumerate(studenci, start=1):
    audytorium = audytoria[i % len(audytoria) - 1]  # cykliczne przypisanie
    przypisania.append((i, student[0], audytorium[0]))  # (id_przypisania, id_studenta, id_audytorium)

# Wstawienie przypisań do tabeli
cursor.executemany(
    "INSERT OR IGNORE INTO przypisania (id_przypisania, id_studenta, id_audytorium) VALUES (?, ?, ?)",
    przypisania
)
conn.commit()

# Pobranie przypisań z nazwami studentów i audytoriów
cursor.execute("""
SELECT p.id_przypisania,
       s.imie || ' ' || s.nazwisko AS student,
       a.nazwa_budynku || ' ' || a.numer_sali AS audytorium
FROM przypisania p
JOIN studenci s ON p.id_studenta = s.id_studenta
JOIN audytoria a ON p.id_audytorium = a.id_audytorium
""")
wyniki = cursor.fetchall()

# Wyświetlenie w formie tabeli
headers = ["ID Przypisania", "Student", "Audytorium"]
print(tabulate(wyniki, headers=headers, tablefmt="grid"))

# Zamknięcie połączenia
conn.close()