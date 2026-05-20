class KalkulatorWalut:
    @staticmethod
    def usd_na_pln(kwota_usd):
        """Konwertuje kwotę w USD na PLN przy stałym kursie 1 USD = 4.0 PLN"""
        kurs = 4.0
        return kwota_usd * kurs
    
    
# Wywołanie metody bez tworzenia obiektu klasy
kwota_w_pln = KalkulatorWalut.usd_na_pln(50)
print(f"50 USD = {kwota_w_pln} PLN")