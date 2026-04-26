from typing import Tuple # import z biblioteki typing, która służy do opisywania typów danych w adnotacji funkcji.

def analiza_listy(lista: list[int]) -> Tuple[int, int, int]:
    """
    Analizuje listę liczb całkowitych i zwraca krotk:
    (minimum, maksimum, suma elementów).

    Parametry:
        lista (list[int]): lista liczb całkowitych
        
    Zwraca:
    Tuple[int, int, int]: krotka (min, max, sum)
    """
    if not lista:
        # jeśli lista jest pusta, można zwrócić None lub zero,
        # tu zwraca (None, None, 0) jako przykład:
        return (None, None, 0)
    
    minimum = min(lista)
    maksimum = max(lista)
    suma = sum(lista)
    
    return (minimum, maksimum, suma)

# Przykład wywołania:
wynik = analiza_listy([3, 7, 1, 9, 4])
print(f"Minimum: {wynik[0]}, Maksimum: {wynik[1]}, Suma: {wynik[2]}")