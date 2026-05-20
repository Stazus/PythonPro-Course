class Uzytkownik:
    def __init__(self, wiek: int):
        self._wiek = None
        self.wiek = wiek  # używamy settera przy inicjalizacji
        
    @property # getter
    def wiek(self):
        return self._wiek
    
    @wiek.setter
    def wiek(self, value):
        if 0 <= value <= 120:
            self._wiek = value
        else:
            print("Błąd: wiek musi być w zakresie 0 - 120 lat!")
            
# przykładowe użycie
u1 = Uzytkownik(25)
print("Wiek uzytkownika: ", u1.wiek)

u1.wiek = 200  # nepoprawny wiek
print("Wiek użytkownika: ", u1.wiek)

u1.wiek = 40   # poprawny wiek
print("Wiek użytkownika: ", u1.wiek)