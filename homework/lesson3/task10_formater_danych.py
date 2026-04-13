dane = input("Podaj swoje imię i nazwisko (np. ' jan kowalski '): ")

dane = dane.strip() # Usunięcie białych znaków z poczatku i końca

dane = dane.title() # Kazde słowo zaczyna się wielka literą

print("Sformatowane dane: ", dane)
print("Długość danych (znaków): ", len(dane))