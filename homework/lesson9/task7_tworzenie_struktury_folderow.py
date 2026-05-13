"""
Program: Tworzenie struktury forderów projekt
Opis:
    Skrypt wykorzystuje moduł pathlib do utworzenia podstawowej struktury folderow
    dla projektu. Tworzone są następujące katalogi:
        - Projekt/src (na pliki źródłowe, np. kod w Pythonie)
        - Projekt/data (na dane wejsciowe, pliki CSVm Json itp.)
        - Projekt/docs (na dokumentację projektu)
        
    Jeśli foldery już istnieją, nie pojawi sie błąd - dzięki metodzie mkdir z
    parametrem exist_ok=True.    
"""

from pathlib import Path

# Tworzymy scieżkę głowną dla projektu
projekt_dir = Path("Projekt")

# Lista podfolderów, które maja zostać utworzone
subfolders = ["src", "data", "docs"]

# Iterujemy po liście i tworzymy foldery wewnątrz katalogu Projektu
for folder in subfolders:
    # Ustalamy pełna ścieżkę do podfolderu
    path = projekt_dir / folder
    
    # Tworzymy katalog (z parametrem exist_ok=True - brak błędu jeśli już istnieje)
    path.mkdir(parents=True, exist_ok=True)
    
    # Informacja dla uzytkownika
    print(f"Utworzono folder: {path}")