tekst = " Python jest super! "

tekst = tekst.strip() # Usunięcie białych znaków na poczaku i na końcu
print("Po usunięciu białych znaków: ", tekst)

tekst = tekst.lower() # przekształcenie całego ciągu na małe litery
print("Po zamianie na małe litery: ", tekst)

tekst = tekst.replace("super", "świetny") # Zamiana słowaq "super" na "świetny"
print("Po zamianie słowa: ", tekst)

print("Znak pod indeksem 4: ", tekst[4]) # Wyświetlenie znaku pod indeksem 4