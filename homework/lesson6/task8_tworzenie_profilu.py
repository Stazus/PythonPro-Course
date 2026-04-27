def stworz_profil(imie, **dane_dodatkowe):
    profil = {'imie': imie, **dane_dodatkowe}
    return profil

# Przykładowe wyświetlenia:
uzytkownik1 = stworz_profil("Anna", wiek=30, miasto="Warszawa", email="anna@example.com")
uzytkownik2 = stworz_profil("Tomek", hobby="szachy", zawod="programista")

print(uzytkownik1)
print(uzytkownik2)