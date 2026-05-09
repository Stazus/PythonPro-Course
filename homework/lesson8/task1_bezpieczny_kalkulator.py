while True: 
    koniec = False # na początku każdej inetracji ustawiamy flagę na False ponieważ domyślnie zakładamy, że program będzie działał dalej
    try:
        a_str = input("Podaj pierwszą liczbę (lub 'q' aby zakończyć): ")
        if a_str.lower() == 'q':
            print("Koniec programu.")
            koniec = True # ustawiamy flagę, że użytkownik chce zakończyć
            break # przerywamy pętlę
        a = float(a_str)
        
        b_str = input("Podaj druga liczbę (lub 'q' aby zakończyć): ")
        if b_str.lower() == 'q':
            print("Koniec programu.")
            koniec = True
            break
        b = float(b_str)
        
        op = input("Podaj operację (+, -, *, /) lub 'q' aby zakończyć: ")
        if op.lower() == 'q':
            print("Koniec programu.")
            koniec = True
            break
        
        if op == "+":
            wynik = a + b
        elif op == "-":
            wynik = a - b
        elif op == "*":
            wynik = a * b
        elif op == "/":
            wynik = a / b
        else:
            print("Nieznana operacja!")
            continue # pomijamy dalszą część i zaczybamy następną iterację, ale finally się wykona
        
    except ValueError:
        print("Błąd: Podaj poprawne liczby.")
    except ZeroDivisionError:
        print("Błąd: Dzielenie przez zero!")
    else: 
        print(f"Wynik: {wynik}")
    finally:
        if not koniec:
            print("Kolejna operacja...\n") # komunikat wyświetli się tylko, jeśli użytkownik nie wybrał 'q' czyli nie chce kończyc    