import multiprocessing


def pobierz_imie(kolejka):
    print("Podaj swoje imię: ", end="", flush=True)

    with open("/dev/tty", "r") as terminal:
        imie = terminal.readline().strip()

    kolejka.put(imie)


if __name__ == "__main__":
    kolejka = multiprocessing.Queue()

    proces = multiprocessing.Process(
        target=pobierz_imie,
        args=(kolejka,),
    )

    proces.start()

    imie = kolejka.get()

    proces.join()

    print(f"Witaj, {imie}!")
