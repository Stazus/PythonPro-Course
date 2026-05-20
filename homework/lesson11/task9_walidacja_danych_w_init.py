class RejestracjaUzytkownika:
    def __init__(self, email, haslo):
        # Walidacja email
        if '@' not in email:
            raise ValueError("Niepoprawny email: brak znaku '@'" )
        # Walidacja hasła
        if len(haslo) < 8:
            raise ValueError("Niepoprawne hasło: musi mieć co najmniej 8 znaków")
        
        self.email = email
        self.haslo = haslo
        
# --- TESTY ---
dane_testowe = [
    ("uzytkownik@example.com", "mojehaslo123"), # poprawne
    ("niepoprawnyemail.com", "mojehaslo123"),   # brak @ w email
    ("test@example.com", "short")               # haslo za krótkie
]
      
for email, haslo in dane_testowe:
    try:
        uzytkownik = RejestracjaUzytkownika(email, haslo)
        print(f"Utworzono użytkownika: {uzytkownik.email}")
    except ValueError as e:
        print(f"Błąd przy tworzeniu użytkownika ({email}): {e}") 