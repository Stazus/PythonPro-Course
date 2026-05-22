"""
Dwie tabele:: Studenci i Audytoria

Skrypt tworzy nową baę danych uczelnia.db i w niej dwie tabele:
1. studenci:
   - id_studenta (INEGER, PRIMARY KEY)
   - imie (TEXT)
   - nazwisko (TEXT)
2. audytoria:
   - id_audytorium (INTEGER, PRIMARY KEY)
   - nazwa_budynku (TEXT)
   - numer_sali (INTEGER)
"""

import sqlite3

# Połączenie z bazą (Jeśli nie istnieje, zostanie utworzona)
conn = sqlite3.connect("uczelnia.db")
cursor = conn.cursor()

# Twprzenie tabeli studenci
cursor.execute("""
CREATE TABLE IF NOT EXISTS studenci (
    id_studenta INTEGER PRIMARY KEY,
    imie TEXT,
    nazwisko TEXT
)
""")

# Tworzenie tabeli audytoria
cursor.execute("""
CREATE TABLE IF NOT EXISTS audytoria (
    id_audytorium INTEGER PRIMARY KEY,
    nazwa_budynku TEXT,
    numer_sali INTEGER
)
""")

# Zatwierdzenie zmian
conn.commit()
print("Baza uczelnia.db została utworzona z tabeli studenci i audytoria.")

# Zamknięcie połączenia
conn.close()