class Figura:
    def oblicz_pole(self):
        pass # metoda bazowa, nic nie robi
    
class Kwadrat(Figura):
    def __init__(self, bok):
        self.bok = bok
        
    def oblicz_pole(self):
        return self.bok * self.bok
    
class Kolo(Figura):
    PI = 3.14159
    
    def __init__(self, promien):
        self.promien = promien
        
    def oblicz_pole(self):
        return self.PI * (self.promien ** 2)
    
# Tworzymy obiekty
kwadrat = Kwadrat(4)
kolo = Kolo(3)

# Lista figur
figury = [kwadrat, kolo]

# polimorfizm - ta sama metoda działa dla rożnych klas
for figura in figury:
    print(f"Pole figury: {figura.oblicz_pole()}")