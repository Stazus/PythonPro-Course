sekret = 42

print("Zgadnij liczbę!")

while True: 
    try:
        liczba = int(input("Podaj liczbę: "))
        
        if liczba == sekret:
            print("Gratulacje! Zgadłeś!")
            break
        else:
            print("To nie ta liczba. Spróbuj jeszcze raz.")
            
    except ValueError:
        print("Błąd: Podaj liczbę całkowitą.")