imiona = ["Anna", "Jan", "Piotr", "Kasia"]

szukane_imie = input("Podaj imię do wyszukiwania: ")

for imie in imiona:
    if imie.lower() == szukane_imie.lower():
        print("Znaleziono!")
        break
else:
    print("Nie znaleziono imienia na liscie.")