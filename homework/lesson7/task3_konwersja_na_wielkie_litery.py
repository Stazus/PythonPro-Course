imiona = ["anna", "piotr", "kasia"]

"""
map() - zwraca obiekt, więc przekształcamy go na listę
str.capitalize - pierwszą literę robi wielką, pozostałe małymi
map(str.capitalize, imiona) - weź każdy element z imiona i zastosuj capitalize
"""

imiona_wielka_litera = list(map(str.capitalize, imiona))

print(imiona_wielka_litera)