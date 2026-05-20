from dataclasses import dataclass

@dataclass
class Film:
    tytuł: str
    rezyser: str
    rok_produkcji: int
    
# tworzenie instancji
film1 = Film("Incepcja", "Christopher Nolan", 2010)
film2 = Film("Matrix", "Lana i Lilly Wachowski", 1999)

# wyświetlanie
print(film1)
print(film2)