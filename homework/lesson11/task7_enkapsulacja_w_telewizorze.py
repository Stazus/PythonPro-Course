class Telewizor:
    def __init__(self):
        self.__kanal = 1
        self.__glosnosc = 10
        self.__wlaczony = False
        
    def wlacz(self):
        self.__wlaczony = True
        print("Telewizor został włączony.")
        
    def wylacz(self):
        self.__wlaczony = False
        print("Telewozor został wyłączony.")
        
    def zmien_kanal(self, numer):
        if self.__wlaczony:
            self.__kanal = numer
            print(f"Zmieniono kanał na {numer}.")
        else:
            print("Nie można zmienić kanału. Telewizor jest wyłączony.")
            
    def glosniej(self):
        if self.__wlaczony:
            if self.__glosnosc < 100:
                self.__glosnosc += 1
            print(f"Głośność: {self.__glosnosc}")
        else:
            print("Telewizor jest wyłączony.")
            
    def ciszej(self):
        if self.__wlaczony:
            if self.__glosnosc > 0:
                self.__glosnosc -= 1
            print(f"Głośność: {self.__glosnosc}")
        else:
            print("Telewizor jest wyłączony.")
            
    def info(self):
        stan = "włączony" if self.__wlaczony else "wyłączony"
        print(f"Telewizor: {stan}, Kanał: {self.__kanal}, Głośność: {self.__glosnosc}")


# --- Test działania ---
tv = Telewizor()
tv.info()

tv.zmien_kanal(5)   # próba zmiany przy wyłączonym TV
tv.glosniej()       # próba zmiany głośności przy wyłączonym TV

tv.wlacz()
tv.zmien_kanal(5)
for _ in range(95): # 95 prób, w tym 5 żeby przekroczyć 100
    tv.glosniej()   # próba przekroczenia głośności powyżej 100
    
tv.ciszej()
tv.info()

tv.wylacz()
tv.info()