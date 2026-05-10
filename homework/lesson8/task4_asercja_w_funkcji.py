import time

def oblicz_srednia(lista_ocen):
    """
    Funkcja oblicza średnia arytmetyczną z listy ocen.
    
    Argumenty:
    lista_ocen -- lista liczb (np. [5, 4, 3, 6])
    
    Zasada działania:
    1. Najpierw sprawdzamy za pomocą asercji, czy lista nie jest pusta.
    assert len(lista_ocen) > 0, "Lista ocen nie może być pusta"
        - Jesli lista jest pusta, program przerwie działanie i zwroci błąd AssertionError.
        - Dzięki temu mamy pewność, że nie spróbujemy dzielić przez zero.
    2. Jeśli lista ma co najmniej jeden element, obliczamy średnią:
        euma elementów / liczba elementów.
    3. Zwracamy obliczoną średnią.
    
    Uwaga:
    W głownym programie po obliczeniu średniej z pierwszej listy dodajemy pauzę (time.sleep),
    aby łatwiej było zauważyć, co sie dzieje zanim przejdziemy do obliczeń dla drugiej listy.
    """
    assert len(lista_ocen) > 0, "Lista ocen nie może być pusta"
    return sum(lista_ocen) / len(lista_ocen)

# Przykładowe dane
oceny1 = [5, 4, 3, 6]
oceny2 = [] # lista pusta - spowoduje błąd AssertionError

# Wywołanie
print("Średnia z ocen 1: ", oblicz_srednia(oceny1))

# Dodajemy przerwę, aby było widać rożnicę w działaniu
time.sleep(3) # pauza 3 sekundy

print("Średnia z ocen 2: ", oblicz_srednia(oceny2)) # tu program się zatrzyma z AssertionError