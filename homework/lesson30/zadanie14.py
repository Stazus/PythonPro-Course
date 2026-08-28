import os
import shutil
import threading


def kopiuj_plik(sciezka_zrodlowa, sciezka_docelowa):
    nazwa_pliku = os.path.basename(sciezka_zrodlowa)

    print(f"Kopiowanie pliku {nazwa_pliku}...")

    shutil.copy2(sciezka_zrodlowa, sciezka_docelowa)

    print(f"Ukończono kopiowanie pliku {nazwa_pliku}")


if __name__ == "__main__":
    katalog_zrodlowy = "katalog_zrodlowy"
    katalog_docelowy = "katalog_docelowy"

    pliki = os.listdir(katalog_zrodlowy)

    watki = []

    for plik in pliki:
        sciezka_zrodlowa = os.path.join(katalog_zrodlowy, plik)
        sciezka_docelowa = os.path.join(katalog_docelowy, plik)

        if os.path.isfile(sciezka_zrodlowa):
            watek = threading.Thread(
                target=kopiuj_plik,
                args=(sciezka_zrodlowa, sciezka_docelowa),
            )

            watki.append(watek)
            watek.start()

    for watek in watki:
        watek.join()

    print("Wszystkie pliki zostały skopiowane.")
