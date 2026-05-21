"""
Wyświetlenie całej biblioteki
Skrypt łączy się z bazą biblioteka.db i pobiera wszystkie rekordy
z tabeli ksiązki, a następnie wyświetla je w konsoli.
"""

import sqlite3

# Połączenie z baza danych
conn = sqlite3.connect("biblioteka.db")
cursor = conn.cursor()

# Pobierz wszystkie książki
cursor.execute("SELECT * FROM ksiazki")
ksiazki = cursor.fetchall()

# Wyświetl w konsoli
print("Zwartość tabeli 'ksiazki': ")
for ks in ksiazki:
    print(ks)
    
# Zamknij połączenie
conn.close()