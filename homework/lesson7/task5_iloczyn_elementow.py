from functools import reduce # Importujemy funkcję reduce z modułu functools

liczby = [1, 2, 3, 4, 5]

iloczyn = reduce(lambda a, b: a * b, liczby)

"""
reduce() steruje procesem: bierz dwa pierwsze elementy i wywołaj lambda; 
potem wynik jest uznawany jako pierwsza wartość, bierze kolejną wartośc z listy 
i znowu wywołuje funkcję aż do końca listy
"""

print("Iloczyn elementów: ", iloczyn)