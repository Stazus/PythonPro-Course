a = 256
b = 256
c = 256

print("Identyfikatory dla wartości 256: ")
print("id(a): ", id(a))
print("id(b): ", id(b))
print("id(c): ", id(c))

x = 257
y = 257
z = 257

print("\nIdentyfikatory dla wartości 257: ")
print("ide(x): ", id(x))
print("id(y): ", id(y))
print("id(z): ", id(z))

# Wyjasnienie
"""
Python optymalizuje i cache'uje małe liczby całkowite od -5 do 256, czyli tzw. "internowanie". Dla tych wartości wszystkie 
zmienne wskazują na ten sam obiekt w pamięci dlatego id(a), id(b), id(c) są takie same
"""

"""
Dla liczb większych niż 256 (jak 257) nie ma gwarancji, że Python użyje tego samego obiektu - zazwyczaj tworzy nowe. 
Dlatego id(x), id(y), id(z) mogą być rożne
"""