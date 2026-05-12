"""
Program prowadzi dziennik wpisów użytkownika
Zapisuje kolejne linie do pliku dziennik.txt
Kończy działanie po wpisaniu "koniec"
"""
plik = "dziennik.txt"

while True:
    wpis = input("Wpisz linię do dziennika (lub 'koniec' aby zakończyć): ")
    if wpis.lower() == "koniec":
        print("Zakończono działanie programu.")
        break
    
    with open(plik, "a", encoding="utf-8") as f: # - append (dopisywanie); tworzy plik jesli nie istnieje; jeśli istnieje -> dopisuje tekst na końcu, nie kasując starych danych.
        f.write(wpis + "\n")

