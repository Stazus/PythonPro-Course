from dataclasses import dataclass

# --- własny wyjątek ---
class BrakSrodkowError(Exception):
    pass

@dataclass
class KontoBankowe:
    _saldo: float = 0.0   # prywatne saldo
    
    @property
    def saldo(self):
        """Zwraca aktualne saldo (tylko odczyt)."""
        return self._saldo
    
    def wplac(self, kwota):
        """Dodaje kwotę do salda. Podnosi ValueError jeśli kwota ujemna."""
        if kwota < 0:
            raise ValueError("Kwota do wypłaty nie może być ujemna!")
        self._saldo += kwota
        print(f"Wpłacono: {kwota}. Nowe saldo: {self._saldo}")
        
    def wyplac(self, kwota):
        """
        Odejmuje kwotę od salda. 
        Podnosi ValueError jeśli kwota ujemna.
        Podnosi BrakSrodkowError jesli brak wystarczających środków.
        """
        if kwota < 0:
            raise ValueError("Kwota do wypłaty nie może być ujemna!")
        if kwota > self._saldo:
            raise BrakSrodkowError("Brak wystarczających środków na koncie!")
        self._saldo -= kwota
        print(f"Wypłacono: {kwota}, Nowe saldo: {self._saldo}")
        
        
# --- Testowanie ---
konto = KontoBankowe()

try:
    konto.wplac(100)
    konto.wyplac(50)
    konto.wyplac(100) # tu powinien wystąpić BrakSrodkowError
except ValueError as ve:
    print("Błąd: ", ve)
except BrakSrodkowError as be:
    print("Błąd: ", be)
    
try:
    konto.wplac(-20) # ValueError
except ValueError as ve:
    print("Błąd: ", ve)
    
print("Aktualne saldo: ", konto.saldo)
    