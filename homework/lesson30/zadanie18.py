import threading
import random


class KontoBankowe:
    def __init__(self, saldo=1000):
        self.saldo = saldo
        self.lock = threading.Lock()

    def wplac(self, kwota):
        with self.lock:
            self.saldo += kwota
            print(f"Wpłata: {kwota} zł | Saldo: {self.saldo} zł")

    def wyplac(self, kwota):
        with self.lock:
            if self.saldo >= kwota:
                self.saldo -= kwota
                print(f"Wypłata: {kwota} zł | Saldo: {self.saldo} zł")
            else:
                print(
                    f"Brak środków na wypłatę {kwota} zł | "
                    f"Saldo: {self.saldo} zł"
                )


def wykonaj_wplate(konto):
    kwota = random.randint(50, 300)
    konto.wplac(kwota)


def wykonaj_wyplate(konto):
    kwota = random.randint(50, 300)
    konto.wyplac(kwota)


if __name__ == "__main__":
    konto = KontoBankowe(1000)

    watki = []

    for _ in range(5):
        watek = threading.Thread(
            target=wykonaj_wplate,
            args=(konto,),
        )
        watki.append(watek)

    for _ in range(5):
        watek = threading.Thread(
            target=wykonaj_wyplate,
            args=(konto,),
        )
        watki.append(watek)

    random.shuffle(watki)

    for watek in watki:
        watek.start()

    for watek in watki:
        watek.join()

    print(f"\nSaldo końcowe: {konto.saldo} zł")
