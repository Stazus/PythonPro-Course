class Produkt:
    def __init__(self, nazwa, cena, kategoria):
        self.nazwa = nazwa
        self.cena = cena
        self.kategoria = kategoria
        
# Tworzymy obiekt klasy Produkt
produkt1 = Produkt("Laptop", 3500, "Elektronika")

# Wydruk atrybutów w osobnych liniach
print(produkt1.nazwa)
print(produkt1.cena)
print(produkt1.kategoria)