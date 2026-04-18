tekst = "Python"
liczba = int(tekst) # ValueError: invalid literal for int() with base 10: 'Python'
print(liczba)

# Wyjasnienie
''' 
liczba = int(tekst) nie można przekonwertować tekstu zawierającego litery na liczbę całkowitą
funkcja int() działa tylko na tekstach, które zawierają cyfry, np. "123"
tekst "Python" zawiera litery, więc konwersja kończy się blędem ValueError
'''