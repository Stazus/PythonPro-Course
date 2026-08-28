import multiprocessing


def oblicz(conn):
    liczby = conn.recv()

    suma = sum(liczby)
    srednia = suma / len(liczby)

    conn.send((suma, srednia))
    conn.close()


if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()

    proces = multiprocessing.Process(
        target=oblicz,
        args=(child_conn,),
    )

    proces.start()

    liczby = [10, 20, 30, 40, 50]

    print(f"Proces nadrzędny wysyła: {liczby}")
    parent_conn.send(liczby)

    suma, srednia = parent_conn.recv()

    proces.join()

    print(f"Suma: {suma}")
    print(f"Średnia: {srednia}")
