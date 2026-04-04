name = input("Jak masz na imię? ") # pytam o imię
age = int(input("Ile masz lat ")) # pytam o wiek i konwertuję stringa (bo integer zawsze zwraca stringa) na inta, bo wiek jest liczbą
print(f"Cześć, {name}! Wiem, że masz {age} lat.") # wyswietlam powitanie