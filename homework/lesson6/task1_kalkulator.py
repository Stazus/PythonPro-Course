def kalkulator(a, b, operacja):
    if operacja == "+":
        return a + b
    elif operacja == "-":
        return a - b
    elif operacja == "*":
        return a * b
    elif operacja == "/":
        if b != 0:
            return a / b
        else:
            return "Błąd: Dzielenie przez zero"
    else:
        return "Błąd: Nieznana operacja"
    
    #Pobieranie danych od użytkownika dla sprawdzenia działania funkcji kalkulator
try:
    a = float(input("Podaj pierwszą liczbę: "))
    b = float(input("Podaj drugą liczbę: "))
    operacja = input("Podaj operację (+, -, *, /): ")

    wynik = kalkulator(a, b, operacja)
    print("Wynik:", wynik)
except ValueError:
    print("Błąd: Nieprawidłowe dane wejściowe. Podaj liczby.")
    
    