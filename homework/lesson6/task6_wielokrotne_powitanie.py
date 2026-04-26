def wielokrotne_powitanie(imie: str, ilosc: int) -> None:
    """
    Wyświetla powitanie 'Cześć, {imie}!' określoną liczbę razy.
    
    Parametry:
        imie (str): imię osoby, którą witamy
        ilosc (int): liczba powitań do wyświetlenia
        
    Zwraca:
        None: funkcja nic nie zwraca, tylko wyświetla tekst
    """
    for _ in range(ilosc):
        print(f"Cześć, {imie}!")
        
    # --- Program główny: pobieranie danych od użytkownika ___
try:
    imie = input("Podaj imię: ")
    ilosc = int(input("Ile razy chcesz się przywitać?: "))
    
    if ilosc <= 0:
        print("Nie wyświetlono powitań, ponieważ liczba powitań jest zero lub ujemna.")
    else:
        wielokrotne_powitanie(imie, ilosc)
        
except ValueError:
    print("Błąd: liczba powitań musi być liczbą całkowitą.")