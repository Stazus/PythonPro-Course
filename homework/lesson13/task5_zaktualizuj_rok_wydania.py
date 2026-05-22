"""
Aktualizacja roku wydania książki

Skrypt łączy się z bazą biblioteka.db i pozwala użytkownikowi:
1. Wybrać użytkownikowi książkę po tytule.
2. Zaktualizować jej rok wydania na nową wartość.
3. Wyswietlić dane książki przed i po aktualizaji, aby potwierdzić zmianę.

Używa parametrów w zapytaniach SQL, aby zabezpieczyć się przed SQL injection.
"""
import sqlite3

# Połączenie z bazą
conn = sqlite3.connect("biblioteka.db")
cursor = conn.cursor()

# Pobierz tytuł książki od użytkwnika
tytul = input("Podaj tytuł książki, której rok wydania chcesz zmienić: ")

# Sprawdzenie czy ksiażka istnieje
cursor.execute("SELECT * FROM ksiazki WHERE tytul = ?", (tytul,))
ksiazka = cursor.fetchone()

if ksiazka:
    print(f"\nAktualne dane ksiazki: {ksiazka}")
    nowy_rok = input("Podaj nowy rok wydania: ")
    
    # Aktualizacja roku wydania
    cursor.execute("UPDATE ksiazki SET rok_wydania = ? WHERE tytul = ?", (nowy_rok, tytul) )
    conn.commit()
    
    # Pobranie zaktualizowanej książki
    cursor.execute("SELECT * FROM ksiazki WHERE tytul = ?", (tytul,))
    zaktualizowana_ksiazka = cursor.fetchone()
    print(f"\nZaktualizowane dane ksiazki: {zaktualizowana_ksiazka}")
else:
    print(f"\nNie znaleziono książki o tytule '{tytul}' w bazie.")
    
# Zamknięcie połączenia
conn.close()