# importujemy moduł datetime, aby móc zapisać w logach datę i godzine wystąpienia błędu
import datetime

# Głowna pętla programu - będzie się wykonywać, dopóki użytkownik nie wpisze 'q'
while True: 
    koniec = False # flaga informująca czy uzytkownik chce zakończyć działanie programu
    
    # otwieramy plik logów w trybie "dopisywania" (append)
    # dzięki temu każdy nowy błąd będzie dodany na końcu pliku log.txt, a nie nadpisze poprzednich wpisów
    # encoding="utf-8" pozwala zapisać polskie znaki
    log_file = open("log.txt", "a", encoding="utf-8")
    
    try:
        # Pobieramy pierwsza liczbę od uzytkownika lub 'q' aby zakończyć
        a_str = input("Podaj pierwszą liczbę (lub 'q' aby zakończyć): ")
        if a_str.lower() == 'q':
            print("Koniec programu.")
            koniec = True
            break # wychodzimy z pętli
        a = float(a_str) # konwersja na liczbę zmiennoprzecinkową
        
        # Pobieramy drugą liczbę
        b_str = input("Podaj drugą liczbę (lub 'q' aby zakończyć): ")
        if b_str.lower() =='q':
            print("Koniec programu.")
            koniec = True
            break
        b = float(b_str)
        
        # Pobieramy operację matematyczną
        op = input("Podaj operację (+, -, *, /) lub 'q' aby zakończyć: ")
        if op.lower() == 'q':
            print("Koniec programu.")
            koniec = True
            break
        
        # Wykonujemy odpowiednia operację
        if op == "+":
            wynik = a + b
        elif op == "-":
            wynik = a - b
        elif op == "*":
            wynik = a * b
        elif op == "/":
            wynik = a / b # UWAGA: może spowodować ZeroDivisionError
        else:
            print("Nieznana operacja!")
            continue # przechodzimy do kolejnej iteracji pętli
        
    except Exception as e:
        # Wyjatek zostanie przechwycony i opisany
        print(f"Błąd: {e}")
        # Zapisujemy datę i godzinę, typ błędu i treść błędu do log.txt
        log_file.write(f"{datetime.datetime.now()} - Błąd: {type(e).__name__} - {e}\n")
        
    else:
        # Jeśli nie było błędu, wyświetlamy wynik
        print(f"Wynik: {wynik}")
        
    finally:
        # finally wykona się zawsze - nawet jesli wystąpi wyjatek lub break
        log_file.close() # Zawsze zamyka plik z logami
        if not koniec:
            print("Kolejna operacja...\n")