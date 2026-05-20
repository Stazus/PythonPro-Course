plik_nazwa = "nieistniejacy.txt"

try:
    with open(plik_nazwa, "r", encoding="utf-8") as f:
        zawartosc = f.read()
        print("Zawartość pliku: ")
        print(zawartosc)
except FileNotFoundError:
    print(f"Błąd: Plik '{plik_nazwa}' nie istnieje!")