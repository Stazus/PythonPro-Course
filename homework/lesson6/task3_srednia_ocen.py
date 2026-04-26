def oblicz_srednia(*args):
    if len(args) == 0:
        return 0
    return sum(args) / len(args)

# --- Przykładowe wywołania ---

print(oblicz_srednia(5, 4, 3))    # wynik: 4.0
print(oblicz_srednia(6))          # wynik: 6.0
print(oblicz_srednia())           # wynik: 0
print(oblicz_srednia(2, 3, 4, 5)) # wynik: 3.5