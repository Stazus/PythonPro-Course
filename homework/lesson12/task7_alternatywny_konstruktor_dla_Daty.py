class Data:
    def __init__(self, dzien, miesiac, rok):
        self.dzien = dzien
        self.miesiac = miesiac
        self.rok = rok
        
    @classmethod
    def ze_stringa(cls, data_string):
        """Tworzy obiekt Data z napisu w formacie 'DD-MM-RRRR'."""
        dzien_str, miesiac_str, rok_str = data_string.split("-")
        return cls(int(dzien_str), int(miesiac_str), int(rok_str))
    
    def __str__(self):
        return f"{self.dzien:02d}-{self.miesiac:02d}-{self.rok}"
    
# Interaktywne wczytywanie daty od użytkownika
data_input = input("Podaj datę w formacie DD-MM-RRRR: ")
try:
    data_obj = Data.ze_stringa(data_input)
    print("Utworzono obiekt DATA: ", data_obj)
except ValueError:
    print("Błąd: podano datę w niepoprawnym formacie. Uzyj DD-MM-RRRR")
    
