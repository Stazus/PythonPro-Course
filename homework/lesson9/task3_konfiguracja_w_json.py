import json

"""
Program: Konfiguracja w JSON

Opis:
Ten program tworzy słowniik z ustawieniami aplikacji (np. użytkownik, motyw, rozdzielczość),
następnie zapisuje go do pliku config.json w formacie FSON z polskimi znakami
i czytelnymi wcięciami. Potem ponownie otwiera plik config.json,
odczytuje jego zawartość i wyświetkla ją na ekranie.
"""
# Tworzymy słownik z ustawieniami aplikacji
konfiguracja = {
    "uzytkownik": "admin",
    "motyw": "ciemny",
    "rozdzielczosc": [1920, 1080]
}

# Nazwa pliku konfiguracyjnego
plik = "config.json"

# ---ZAPIS DO PLIKU JSON ---
with open(plik, "w", encoding="utf-8") as f:
    # ensure_ascii=False -> zachowuje polskie znaki
    # indent=4 -> dodaje wcięcia dla czytelności
    json.dump(konfiguracja, f, ensure_ascii=False, indent=4)
    
print(f"Plik {plik} został zapisany.")


# --- ODCZYT z PLIKU JSON ---
with open(plik, "r", encoding="utf-8") as f:
    odczytana_konfiguracja = json.load(f)
    
print("Odczytana konfiguracja: ")
print(odczytana_konfiguracja)