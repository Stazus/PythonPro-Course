a = int(input("Podaj pierwszą wartość logiczną (1 dla True, 0 dla False): "))
b = int(input("Podaj drugą wartość logiczną (1 dla true, 0 dla False): "))

# Konwersja liczb na wartości logiczne za pomocą if-lese
if a == 1:
    a_bool = True
else:
    a_bool = False
    
if b == 1:
    b_bool = True
else:
    b_bool = False
    
# Operacje logiczne
and_wynik = a_bool and b_bool
or_wynik = a_bool or b_bool

print(f"Wynik AND: {and_wynik}")
print(f"Wynik OR: {or_wynik}")