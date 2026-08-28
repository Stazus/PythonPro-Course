import threading


lista = []
lock = threading.Lock()


def dodaj_jedynki():
    for _ in range(100_000):
        with lock:
            lista.append(1)


def dodaj_dwojki():
    for _ in range(100_000):
        with lock:
            lista.append(2)


watek1 = threading.Thread(target=dodaj_jedynki)
watek2 = threading.Thread(target=dodaj_dwojki)

watek1.start()
watek2.start()

watek1.join()
watek2.join()

print(f"Długość listy: {len(lista)}")
print(f"Czy lista ma 200000 elementów? {len(lista) == 200_000}")
