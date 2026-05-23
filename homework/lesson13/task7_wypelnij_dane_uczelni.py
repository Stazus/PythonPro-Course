"""
Skrypt wypełnia tabele studenci i audytoria przykładowymi danymi w bazie uczelnia.db:
- co najmniej 4 studentów
- co najmniej 3 audytoria

Nastepnie pobiera i wyświetla wszystkie dane z obu tabel w formie czytelnych tabel,
aby potwierdzić wprowadzenie danych.
"""

import sqlite3
from tabulate import tabulate

# Połączenie z bazą
conn = sqlite3.connect("uczelnia.db")
cursor = conn.cursor()

# Przykładowi studenci (id_studenta, imię, nazwisko)
studenci = [
    (1, "Anna", "Kowalska"),
    (2, "Jan", "Nowak"),
    (3, "Marta", "Wiśniewska"),
    (4, "Piotr", "Lewandowski")
]

# Przykładowe audytoria (id_audytorium, nazwa_budynku, numer_sali)
audytoria = [
    (1, "A", 101),
    (2, "B", 202),
    (3, "C", 303)
]
# Wstawienie studentów do tabeli
cursor.executemany("INSERT OR IGNORE INTO studenci (id_studenta, imie, nazwisko) VALUES (?, ?, ?)", studenci)

# Wstawienie audytorów do tabeli
cursor.executemany("INSERT OR IGNORE INTO audytoria (id_audytorium, nazwa_budynku, numer_sali) VALUES (?, ?, ?)", audytoria)

# Zatwierdzenie zmian
conn.commit()
print("Tabela studenci i audytoria została wypełniona przykładowymi danymi.\n")

# Wyswietlenie wsystkich studentów w formie tabeli
cursor.execute("SELECT * FROM studenci")
studenci_wyniki = cursor.fetchall()
print("Lista studentów: ")
print(tabulate(studenci_wyniki, headers=["ID Studenta", "Imię", "Nazwisko"], tablefmt="grid"))

print("\nLista audytiriów: ")
cursor.execute("SELECT * FROM audytoria")
audytoria_wyniki = cursor.fetchall()
print(tabulate(audytoria_wyniki, headers=["ID Audytorium", "Nazwa Budynku", "Numer Sali"], tablefmt="grid"))

# Zamknięcie połączenia
conn.close()