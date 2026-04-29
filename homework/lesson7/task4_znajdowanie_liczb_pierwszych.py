def czy_pierwsza(n):
    if n < 2: # Liczby mniejsze niż 2 (czyli 0 i 1) nie są pierwsze - 2 jest liczbą pierwszą, bo dzieli sie przez 1 i siebie samą
        return False
    
    for i in range(2, n): # range(2, 2) pętla nie wykona się dla 2 więc nie bedzie False dla 2; funkcja przejdzie dalej i zwróci True
        if n % i == 0: # Jeśli n jest podzielne przez i (bez reszty), to nie jest liczbą pierwszą
            return False
        
    return True # Jeśli nie znaleźliśmy żadnego dzielnika, to n jest liczbą pierwszą

liczby = list(range(1, 31))

pierwsze = list(filter(czy_pierwsza, liczby))

print("Lista podstawowa: ", liczby)
print("Liczby pierwsze z listy podstawowej: ", pierwsze)