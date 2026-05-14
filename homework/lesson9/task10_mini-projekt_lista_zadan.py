import json
import os

"""
Mini-projekt: Lista zadań
-------------------------
Prosta aplikacja do zarządzania listą zadań. Program:
1. Przy starcie wczytuje istniejśce zadania z pliku zadania.json (jeśli istnieje).
2. Pozwala użytkownikowi:
   - dodać nowe zadanie,
   - wyświetlić wszystkie zadania,
   - zakończyć program zapisując aktualną listę zadań.
3. Przy zamknięciu zapisuje wszystkie zadania do pliku zadania.json.
"""

# Nazwa pliku, w którym będą przechowywane zadania
PLIK_ZADANIA = "zadania.json"

# Funkcja wczytująca zadania z pliku
def wczytaj_zadania():
    if os.path.exists(PLIK_ZADANIA):
        with open(PLIK_ZADANIA, "r", encoding="utf-8") as f:
            return json.load(f)
    return [] # jeśli plik nie istnieje, zwróć pustą listę

# Funkcja zapisująca zadania do pliku
def zapisz_zadania(zadania):
    with open(PLIK_ZADANIA, "w", encoding="utf-8") as f:
        json.dump(zadania, f, indent=4, ensure_ascii=False)
        
# Funkcja dodająca nowe zadanie
def dodaj_zadanie(zadania):
    nowa = input("Podaj treść nowego zadania: ")
    if nowa.strip(): # upewnij się, że nie dodajemy pustego zadania
        zadania.append(nowa.strip())
        print(f"Zadanie '{nowa}' zostało dodane.")
    else:
        print("Nie można dodać pustego zadania.")
        
# Funkcja wyświetlająca wszystkie zadania
def wyswietl_zadania(zadania):
    if not zadania:
        print("Brak zadań na liście.")
    else:
        print("Lista zadań: ")
        for i, zadanie in enumerate(zadania, 1):
            print(f"{i}. {zadanie}")
            
# Główna pętla programu
def main():
    zadania = wczytaj_zadania() # wczytanie istniejących zdań
    
    while True:
        print("\nOpcje: ")
        print("1 - Dodaj zadanie")
        print("2 - Wuswietl wszystkie zadania")
        print("3 - Zakończ program")
        wybor = input("Wybierz opcję: ")
        
        if wybor == "1":
            dodaj_zadanie(zadania)
        elif wybor == "2":
            wyswietl_zadania(zadania)
        elif wybor == "3":
            zapisz_zadania(zadania)
            print("Zadania zapisane. Do widzenia!")
            break
        else:
            print("Niepoprawna opcja, spróbuj ponownie.")
            
if __name__ == "__main__":
    main()