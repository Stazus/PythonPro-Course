"""
Dodawanie książek do tabeli 'ksiazki'
Opis:
Ten skrypt ączy się z bazą danych 'biblioteka.db' i dodaje trzy przykładowe 
książki do tabeli 'ksiazki' za pomocą metody executemany.
"""

import sqlite3

# Połączenie z bazą danych
conn = sqlite3.connect("biblioteka.db")
cursor = conn.cursor()

# Lista książek do dodania
nowe_ksiazki = [
    ("Quo Vadis", "Henryk Sienkiewicz", 1896),
    ("Krzyżacy", "Henryk Sienkiewicz", 1900),
    ("Solaris", "Stanisław Lem", 1961)
]

# Dodanie wielu rekordów naraz
cursor.executemany("INSERT INTO ksiazki (tytul, autor, rok_wydania) VALUES (?, ?, ?)", nowe_ksiazki)

# Zapis zmian
conn.commit()

print("Dodano 3 nowe książki do tabeli 'ksiazki'.")

# Wyswietlenie wszystkich rekordów w tabeli
cursor.execute("SELECT * FROM ksiazki")
for ksiazka in cursor.fetchall():
    print(ksiazka)
    
# Zamknięcie połączenia
conn.close()