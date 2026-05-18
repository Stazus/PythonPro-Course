class Wektor2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Wektor2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Wektor2D(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    
# Testowanie działania
wektor1 = Wektor2D(3, 5)
wektor2 = Wektor2D(1, 2)
    
print("Wektor1: ", wektor1)
print("Wektor2: ", wektor2)

print("Dodawanie: ", wektor1 + wektor2)
print("Odejmowanie: ", wektor1 - wektor2)
print("Czy równe?", wektor1 == wektor2)
print("Czy równe?", wektor1 == Wektor2D(3,5))
    
    
    