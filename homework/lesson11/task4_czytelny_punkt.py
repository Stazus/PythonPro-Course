class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    
# Stworzenie obiektów klasy Punkt
p1 = Punkt(3, 7)
p2 = Punkt(-2, 5)

# Wyświetlenie punktów
print(p1)
print(p2)