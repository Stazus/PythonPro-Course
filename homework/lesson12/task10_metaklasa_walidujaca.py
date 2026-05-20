# --- Metaklasa ---
class MetaWalidujMetody(type):
    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            # sprawdzamy tylko funkcje/metody, ignorujemy magiczne metody
            if callable(attr_value) and not attr_name.startswith("__"):
                if not attr_value.__doc__:
                    raise TypeError(f"Metoda '{attr_name}' w klasie '{name}' wymaga dokumentacji (docstring)!")
        return super().__new__(cls, name, bases, dct)


# --- Przykład poprawnej klasy ---
class Poprawna(metaclass=MetaWalidujMetody):
    def metoda1(self):
        """To jest poprawny docstring."""
        return 42

    def metoda2(self):
        """Kolejna metoda z docstringiem."""
        return "hello"


# --- Przykład klasy z brakującym docstringiem ---
try:
    class Niepoprawna(metaclass=MetaWalidujMetody):
        def metoda1(self):
            """Metoda z docstringiem."""
            return 1

        def metoda2(self):
            return 2  # brak docstringa -> powinien wywołać TypeError
except TypeError as e:
    print("Błąd:", e)


# --- Testowanie działania ---
p = Poprawna()
print(p.metoda1())
print(p.metoda2())