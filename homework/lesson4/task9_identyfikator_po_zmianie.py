x = 10
print("Wartość x: ", x)
print("ID x przed zmianą: ", id(x))

# Zmiana wartości x
x = x + 1
print("Wartość x po zmianie: ", x)
print("ID x po zmianie: ", id(x))

# Komentarz
"""
Zmienna x początkowo wskazuje na obiekt liczbowy 10.
Po wykonaniu operacji x = x + 1 przypisujemy nowy obiekt liczbowy 11.
Każda zmienna tworzy nowy obiekt.
Z tego powodu identyfikator (id) zmiennej x ulega zmianie.
"""