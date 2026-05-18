class Instrument:
    def graj(self):
        return "Wydaje dźwięk."
    
class Strunowy(Instrument):
    def graj(self):
        return super().graj() + " [Szarpnięcie struny]"
    
class Dety(Instrument):
    def graj(self):
        return super().graj() + " [Dżwięk wydobyty z ustnika]"
    
class Gitara(Strunowy):
    def graj(self):
        return super().graj() + " [Akord G-dur]"
    
class Trabka(Dety):
    def graj(self):
        return super().graj() + " [Melodia jazzowa]"
    
    
# --- TESTY ---
instrument = Instrument()
print("Instrument: ", instrument.graj())

strunowy = Strunowy()
print("Strunowy: ", strunowy.graj())

gitara = Gitara()
print("Gitara: ", gitara.graj())

dety = Dety()
print("Dety: ", dety.graj())

trabka = Trabka()
print("Trąbka: ", trabka.graj())