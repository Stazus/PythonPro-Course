while True:
    try:
        # Pobranie wieku psa jako liczby całkowitej
        wiek_psa = int(input("Podaj wiek psa w latach: "))
        
        # Sprawdzenie czy wiek jest większy niż 0
        if wiek_psa > 0:
            break # Poprawna wartość - wyjście z pętli
        else:
            print("Wiek musi być większy biż 0. Spróbuj jeszcze raz.")
            
    except ValueError:
        # Obsługa sytuacji, gdy użytkownik wpisze np. litery
        print("To nie jest poprawna liczba całko0wita. Spróbuj ponownie.")
        
# Obliczenie wieku psa w "ludzkich" latach
if wiek_psa == 1:
    wiek_ludzki = 15
elif wiek_psa == 2:
    wiek_ludzki = 15 + 9
else:
    wiek_ludzki = 15 + 9 + (wiek_psa - 2) * 5
    
print("Wiek psa w ludzkich latach to: ", wiek_ludzki)