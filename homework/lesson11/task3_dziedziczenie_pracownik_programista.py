class Pracownik:
    def __init__(self, imie, stawka_godzinowa):
        self.imie = imie
        self.stawka_godzinowa = stawka_godzinowa
        
    def oblicz_pensje(self, liczba_godzin):
        return self.stawka_godzinowa * liczba_godzin
    
    
class Programista(Pracownik):
    def __init__(self, imie, stawka_godzinowa, jezyki_programowania):
        super().__init__(imie, stawka_godzinowa)
        self.jezyki_programowania = jezyki_programowania
        
        
# Stworzenie obiektu klasy Programista
prog = Programista("Stanisław", 80, ["Python", "JavaScript", "C++"])

# Wywołanie metody oblicz_pensje
print(f"Pensja {prog.imie} wynosi: {prog.oblicz_pensje(160)} zł")
print(f"Jezyki programopwania: {', '.join(prog.jezyki_programowania)}")