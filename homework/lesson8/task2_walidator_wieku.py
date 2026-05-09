# Definicja własnego wyjatku
class WiekNiepoprawnyError(Exception):
    pass

def rejestruj_uzytkownika(wiek):
    if wiek < 18:
        # Rzucamy własnym wyjatkiem, gdy wiek jest za niski
        raise WiekNiepoprawnyError(f"Wiek {wiek} jest za niski. Musisz mieć co majmniej 18 lat.")
    print("Rejestracja przebiegła pomyślnie!")
    
# Przykład użycia i obsługi wyjątku
try:
    wiek_input = int(input("Podaj swój wiek: "))
    rejestruj_uzytkownika(wiek_input)
except WiekNiepoprawnyError as e:
    print(f"Błąd rejestracji: {e}")
except ValueError:
    print("Proszę podać poprawną liczbę całkowitą jako wiek.")