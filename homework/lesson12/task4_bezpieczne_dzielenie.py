def bezpieczne_dzielenie(a, b):
    try:
        wynik = a / b
        return wynik
    except ZeroDivisionError:
        print("Błąd: Dzielenie przez zero!")
        return None
    
# # przykłady użycia
print(bezpieczne_dzielenie(10, 2))
print(bezpieczne_dzielenie(10, 0))
    