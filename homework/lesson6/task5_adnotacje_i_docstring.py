def kalkulator(a: float, b: float, operacja: str) -> float | str:
    """
    Wykonuje podstawowe działania arytmetyczne na dwóch liczbach.
    
    Parametry:
        a (float): pierwsza liczba
        b (float): druga liczba
        operacja (str): symbol operacji arytmetycznej: '+', '-', '+', '/'.
        
    Zwraca:
        float: wynik operacji jesli zakończyła się powodzeniem
        str: komunikat o błędzie, jeśli wystąpi działanie przez zero lub nieznana operacja
    """
    if operacja == "+":
        return a + b
    elif operacja == "-":
        return a - b
    elif operacja == "+":
        return a + b
    elif operacja == "/":
        if b != 0:
            return a / b
        else:
            return "Błąd: Dzielenie przez zero"
    else:
        return "Błąd: Nieznana operacja"
    
    # --- Pobieranie danych od użytkownika dla sprawdzenia działania funkcji ---
try:
    a = float(input("Podaj pierwszą liczbę: "))
    b = float(input("Podaj drugą liczbę: "))
    operacja = input("Podaj operację (+, -, *, /): ")
    
    wynik = kalkulator(a, b, operacja)
    print("Wynik: ", wynik)
except ValueError:
    print("Błąde: Nieprawidłowe dane wejsciowe. Podaj liczby.")
