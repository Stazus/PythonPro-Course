import hashlib
import multiprocessing
import os


def oblicz_hash(sciezka):
    sha256 = hashlib.sha256()

    with open(sciezka, "rb") as plik:
        while True:
            fragment = plik.read(4096)

            if not fragment:
                break

            sha256.update(fragment)

    nazwa_pliku = os.path.basename(sciezka)

    return nazwa_pliku, sha256.hexdigest()


if __name__ == "__main__":
    katalog = "katalog_zrodlowy"

    pliki = [
        os.path.join(katalog, nazwa)
        for nazwa in os.listdir(katalog)
        if os.path.isfile(os.path.join(katalog, nazwa))
    ]

    with multiprocessing.Pool() as pool:
        wyniki = pool.map(oblicz_hash, pliki)

    hashe = dict(wyniki)

    print("Hashe SHA256 plików:")

    for nazwa, hash_pliku in hashe.items():
        print(f"{nazwa}: {hash_pliku}")

    print("\nSłownik:")
    print(hashe)
