"""
Import z CSV i obliczanie cen produktów

Opis działania:
1. Program odczytuje plik 'produkty.csv', w którym znajdują się dane produktów.
2. Używa scv.DoctReader, aby odwołać sie do kolumn po nazwach.
3. Iteruje przez wszystkie wiersze i sumuje ceny produktów.
4. Wyświetla sumę cen wszystkich produktów.
"""

import csv

plik_csv = "produkty.csv"

# zmienna do sumowania cen
suma_cen = 0.0

# otwarcie pliku CSV w trybie odczytu
with open(plik_csv, mode="r", encoding="utf-8") as f:
    # utworzenie obiektu DictReader - umożliwia odwołanie do kolumn po nagłówkach
    reader = csv.DictReader(f)
    
    # iteracja przez wzystkie wiersze
    for wiersz in reader:
        # konwersja wartości kolumny 'cena' na float i dodanie do sumy
        cena = float(wiersz["cena"])
        suma_cen += cena
        
# wyświetlenie sumy cen
print(f"Suma cen wszystkich produktów: {suma_cen:.2f} zł")