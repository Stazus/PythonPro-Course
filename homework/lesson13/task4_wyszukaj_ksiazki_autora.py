"""
Skrypt łączy się z bazą biblioteka.db i pobiera książki danego autora
z tabeli ksiazki. Autor podawany jest przez użytkownika w konsoli. 
"""

import sqlite3

# Połączenie z bazą
conn = sqlite3.connect("biblioteka.db")
cursor = conn.cursor()

# Pobierz autora od użytkownika
autor = input("Podaj imię i nazwisko autora, którego książki chcesz zobaczyć: ")

# Zapytanie SQL z parametrem (zabezpieczenie przed SQL injection)
cursor.execute("SELECT * FROM ksiazki WHERE autor = ?", (autor,))
wyniki = cursor.fetchall()

# Wyświetlenie wyników
if wyniki:
    print(f"\nKsiążki autora {autor}:")
    for ks in wyniki:
        print(ks)
else:
    print(f"\nBrak książek autora {autor} w bazie.")
    
# Zamknij połączenie
conn.close()