"""
Biblioteka - tabela książek
Opis:
Ten skrypt tworzy bazę danych 'biblioteka.db' oraz tabelę 'ksiązki' z kolumnami:
- id (INTEGER, klucz główny, autoinkrementacja)
- tytul (TEXT, mie może być pusty)
- autor (TEXT, nie może być pusty)
- rok_wydania (INTEGER)

Dodatkowo program dodaje przykładowe książki do tabeli i wypisuje ich zawartość w konsoli.  
"""
import sqlite3

# Połączenie z bazą (utworzony plik biblioteka.db, jesli nie istnieje)
conn = sqlite3.connect("biblioteka.db")
cursor = conn.cursor()

# Tworzenie tabeli ksiazki
cursor.execute("""
CREATE TABLE IF NOT EXISTS ksiazki (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   tytul TEXT MOT NULL,
   autor TEXT NOT NULL,
   rok_wydania INTEGER
)
""")

print("Tabela 'ksiazki' została utworzona (jeśli wcześniej nie istniała)'")

# Wstawianie przykładowych rekordów
cursor.execute("INSERT INTO ksiazki (tytul, autor, rok_wydania) VALUES (?, ?, ?)",
               ("Lalka", "Bolesław Prus", 1890))
cursor.execute("INSERT INTO ksiazki (tytul, autor, rok_wydania) VALUES (?, ?, ?)",
               ("Pan Tadeusz", "Adam Mickiewicz", 1834))
cursor.execute("INSERT INTO ksiazki (tytul, autor, rok_wydania) VALUES (?, ?, ?)",
               ("Ferdydurke", "Witold Gombrowicz", 1937))

# Zapis zmian
conn.commit()

# Pobranie i wyświetlenie wszystkich rekordów
cursor.execute("SELECT * FROM ksiazki")
ksiazki = cursor.fetchall()

print("\nZawartość tabeli ksiazki: ")
for ks in ksiazki:
    print(ks)
    
# Zamknięcie połączenia
conn.close()