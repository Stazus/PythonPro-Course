uzytkownicy = [
    {"imie": "Jan", "wiek": 30, "aktywny": True},
    {"imie": "Anna", "wiek": 17, "aktywny": False},
    {"imie": "Piotr", "wiek": 25, "aktywny": True}
]

imiona = [u["imie"].upper() for u in uzytkownicy if u["wiek"] >= 18 and u["aktywny"]] # Dla każdego u z listy, który spełnia warunek — dodaj do wyniku u["imie"].upper()


print(imiona)