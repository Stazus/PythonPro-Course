"""
Program: Eksport listy słowników do pliku CSV

Opis działania
1. Program posiada listę słowników 'produkty', gdzie każdy słownik
   reprezentuje produkt z polami 'nazwa' i 'cena'.
2. Tworzy plik CSV o nazwie 'produkty.csv'.
3. Pierwszy wiersz pliku zawiera nagłowki: 'nazwa' i 'cena'.
4. Kolejne wiersze zawierają dane produktów.
5. Kodowanie UTF-8 zapewnia poprawne zapisanie polskich znaków.
"""

import csv # moduł do obsługi plików CSV

# lista produktów jako słowniki
produkty = [
    {"nazwa": "Mleko", "cena": 3.50},
    {"nazwa": "Chleb", "cena": 4.80}
]

# nazwa pliku CSV
plik_csv = "produkty.csv"

# otwarcie pliku CSV w trybie zapisu
with open(plik_csv, mode="w", newline="", encoding="utf-8") as f:
    # definiujemy nagłówki (klucze słowników)
    naglowki = ["nazwa", "cena"]
    
    # tworzymy obiekt DictWriter, który zapisuje słowniki do CSV
    writer = csv.DictWriter(f, fieldnames=naglowki)
    
    # zapis nagłowków do pierwszego wiersza pliku
    writer.writeheader()
    
    # zapis danych produktów jako kolejne wiersze
    writer.writerows(produkty)
    
# komunikat o zakończeniu zapisu
print(f"Dane zapisano do pliku {plik_csv}")