import threading


def praca_watku(numer):
    print(f"Jestem wątkiem numer {numer}")


watki = []

for numer in range(1, 6):
    watek = threading.Thread(
        target=praca_watku,
        args=(numer,),
    )
    watki.append(watek)
    watek.start()

for watek in watki:
    watek.join()

print("Wszystkie wątki zakończyły pracę.")
