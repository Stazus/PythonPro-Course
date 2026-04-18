lista1 = [1, 1]
lista2 = [1, 1]

print("lista1 == lista2: ", lista1 == lista2) # Sprawdza czy zawartość list jest taka sama
print("lista1 is lista2: ", lista1 is lista2) # Sprawdza czy to ten sam obiekt w pamięci

# Wyjasnienie
"""
Operator == sprawdza równość wartości (czy zawartość listy1 i listy2 jest taka sama)
Operator is sprawdza tożsamość obiektów (czy obie zmienne wskazują na dokładnie ten sam obiekt w pamięci)
Mimo, że obie listy mają tę samą zawartość, są to dwa różne obiekty
"""