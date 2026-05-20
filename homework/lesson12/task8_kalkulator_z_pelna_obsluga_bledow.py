while True:
    try:
        a_input = input("Podaj pierwszą liczbę (lub 'exit' aby zakończyć): ")
        if a_input.lower() == "exit":
            print("Koniec programu.")
            break
        a = float(a_input)
    
        operacja = input("Podaj operację (+, -, *, /): ")
        if operacja.lower() == "exit":
            print("Koniec programu.")
            break
        
        b_input = input("Podaj drugę liczbę: ")
        if b_input.lower() == "exit":
            print("Koniec programu.")
            break
        b = float(b_input)
        
        if operacja == "+":
            wynik = a + b
        elif operacja == "-":
            wynik = a - b
        elif operacja == "*":
            wynik = a * b
        elif operacja == "/":
            wynik = a / b
        else:
            print("Nieznana operacja!")
            continue
    
    except ValueError:
        print("Błąd: podano niepoprawną liczbę!")
    except ZeroDivisionError:
        print("Błąd: dzielenie przez zero!")
    except KeyboardInterrupt:
        print("\nKoniec programu (przerwano przez Ctrl+C)")
        break
    else:
        print("Wyniki: ", wynik)
    finally:
        print("Koniec obliczeń.\n")