def opis_ksiazki(tytul, autor, rok_wydania=2024):
    return f"Książka '{tytul}' została napisana przez {autor} i wydana w roku {rok_wydania}."

# Wywołanie funkcji z argumentami pozycyjnymi (kolejność ma znaczenie)
print(opis_ksiazki("Lalka", "Bolesław Prus"))

# Wywołanie funkcji z argumentami nazwanymi (kolejność nie ma znaczenia)
print(opis_ksiazki(tytul = "Zbrodnia i kara", autor = "Fiodor Dostojewski", rok_wydania = 1866))

# Mieszane argumenty: pozycje + nazwy
print(opis_ksiazki("Hobbit", "J.R.R. Tolkien", rok_wydania = 1937))

# ---Wyjaśnienie---
"""
Argumenty pozycyjne są przekazywane w ustalonej kolejności,
przykład: opis_ksiazki("Lalka", "Bolesław Prus"

Argumenty nazwane - kolejność nie ma znaczenia, bo jest podana nazwa argumentu,
przykład: opis_ksiazki(autor = "Bolesław Prus", tytuł = "Lalka", rok_pwydania = 1890)

Ważne: najpierw muszą byc argumenty pozycyjne, a dopiero potem nazwane
"""