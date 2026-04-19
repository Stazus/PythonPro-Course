cena_bazowa = 100

# Pętla do skutku - poprawny wiek
while True:
    try:
        wiek = int(input("Podaj swój wiek: "))
        if wiek <= 0:
            print("Błąd: wiek musi być większy niż 0. Spróbuj ponownie. ")
        else:
            break
    except ValueError:
        print("Błąd: wiek musi być liczba całkowitą. Spróbuj ponownie.")
        
# Domyślnie: nie jest studentem
student = "nie"

# Jeśli wiek >+ 18, pytamy o status studenta
if wiek >= 18:
    while True:
        student = input("Czy jesteś studentem? (tak/nie): ").strip().lower()
        if student in ["tak", "nie"]:
            break
        else:
            print("Błąd: odpowiedz tylko 'tak' lub 'nie'. Spróbuj ponownie")
            
# Logika z użyciem operatorów 'or' i 'and'
# Zniżka należy się jeśli (wiek < 18) lub (wiek>= 18 i jest studentem)
if wiek < 18 or (wiek >= 18 and student == "tak"):
    cena_koncowa = cena_bazowa * 0.5
    print("Przysługuje ci zniżka 50%.")
else:
    cena_koncowa = cena_bazowa
    print("Nie przysługuje ci zniżka.")
    
#Wyświetlenie końcowej ceny
print(f"Do zapłaty: {cena_koncowa:.2f} PLN")
                  