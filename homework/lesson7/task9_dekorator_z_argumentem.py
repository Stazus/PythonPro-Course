def powtorz(n): # To jest funkcja dekoratora przyjmująca argument n
    def dekorator(funkcja): # To jest właściwy dekorator
        def opakowanie(*args, **kwargs):
            for _ in range(n):
                funkcja(*args, **kwargs)
        return opakowanie
    return dekorator

#Przykład wywołania
@powtorz(3)
def przywitaj():
    print("Cześć!")
    
przywitaj()