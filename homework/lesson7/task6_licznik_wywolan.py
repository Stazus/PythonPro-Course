def stworz_licznik():
    licznik = 0
    """
    stworz_licznik() tworzy zmienną licznik: To jest zmienna lokalna funkcji stworz_licznik(). Normalnie taka zmienna przestaje istnieć, gdy funkcja sie kończy.
    W środku stworz_licznik() tworzona jest funkcja zwieksz(): Ona korzysta z tej zmiennej licznik.
    """
    def zwieksz():
        nonlocal licznik
        """Słowo nonlocal licznik: Mówi Pythonowi "chcę używać zmiennej licznik z zewnetrznej funkcji. Bez nonlocal nie można byłoby zmieniać tej zmiennej (tylko odczytać).
        Funkcja zwieksz() jest zwracana na zewnątrz, a wraz z nią Python „zabiera” zmienną licznik, tworząc closure, dzięki czemu funkcja zapamiętuje jej wartość nawet po zakończeniu działania stworz_licznik().
        """
        licznik += 1
        return licznik
    
    return zwieksz
"""
return zwieksz: Funkcja stworz_licznik() zwraca funkcję zwieksz() - ale nie wywołuje jej jeszcze.
"""

# Użycie:
moj_licznik = stworz_licznik() # Tworzymy nowy licznik (closure) - WYWOŁANIE stworz_licznik(), która tworzy licznik 0, tworzy funkcję zwieksz() i zwraca funkcje zwieksz

print(moj_licznik()) # 1 - pierwsze wywołanie funkcji zwieksz(), licznik = 1; WYWOŁANIE zwieksz(), licznik się swiększa i trafia do print()
print(moj_licznik()) # 2 - wywołanie, licznik = 2
"""
2 - drugie wywołanie, licznik = 2; Python „pamięta” zmienną licznik, ponieważ funkcja zwieksz() nadal ma do niej referencję 
(„wie gdzie w pamięci znajduje się dana wartość” i może z niej korzystać) i modyfikuje jej wartość przy każdym wywołaniu
"""
print(moj_licznik()) # 3 - trzecie wywołanie, licznik = 3