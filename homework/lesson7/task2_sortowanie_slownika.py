oceny = {"Jan": 4, "Anna": 5, "Piotr": 4, "Kasia": 4}

"""
oceny.items() - zwraca pary (klucz, wartość)
key=lambda item: item[1] - oznacza, że sortujemy po drugim elemencie krotki, czyli po ocenie
reverse=True - sortowanie malejace (od najwyższej oceny do najniższej)
"""
posortowane_oceny = sorted(oceny.items(), key=lambda item: item[1], reverse=True)
print(posortowane_oceny)