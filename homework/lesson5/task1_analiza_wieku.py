try:
    wiek = int(input("Podaj swój wiek: "))
    
    if wiek < 0:
        print("Wiek nie może być ujemny.")
    elif wiek <= 1:
        print("Niemowlę")
    elif wiek <= 12:
        print("Dziecko")
    elif wiek <= 17:
        print("Nastolatek")
    elif wiek <= 64:
        print("Dorosły")
    else:
        print("Senior")
        
except ValueError:
    print("Błąd: Wprowadź poprawną liczbę całkowitą.")