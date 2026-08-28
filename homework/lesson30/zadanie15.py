import queue
import threading
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse


START_URL = "https://example.com"
MAX_STRON = 50
LICZBA_WATKOW = 5

kolejka = queue.Queue()
odwiedzone = set()
lock = threading.Lock()


class ParserLinkow(HTMLParser):
    def __init__(self):
        super().__init__()
        self.linki = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for nazwa, wartosc in attrs:
                if nazwa == "href" and wartosc:
                    self.linki.append(wartosc)


def pobierz_strone(url):
    try:
        print(f"Pobieranie: {url}")

        with urllib.request.urlopen(url, timeout=5) as odpowiedz:
            html = odpowiedz.read().decode("utf-8", errors="ignore")

        parser = ParserLinkow()
        parser.feed(html)

        domena_startowa = urlparse(START_URL).netloc

        for link in parser.linki:
            pelny_url = urljoin(url, link)
            parsed = urlparse(pelny_url)

            if parsed.netloc != domena_startowa:
                continue

            pelny_url = parsed._replace(fragment="").geturl()

            with lock:
                if (
                    pelny_url not in odwiedzone
                    and len(odwiedzone) < MAX_STRON
                ):
                    odwiedzone.add(pelny_url)
                    kolejka.put(pelny_url)

    except Exception as blad:
        print(f"Błąd podczas pobierania {url}: {blad}")


def pracownik():
    while True:
        url = kolejka.get()

        if url is None:
            kolejka.task_done()
            break

        pobierz_strone(url)
        kolejka.task_done()


if __name__ == "__main__":
    odwiedzone.add(START_URL)
    kolejka.put(START_URL)

    watki = []

    for _ in range(LICZBA_WATKOW):
        watek = threading.Thread(target=pracownik)
        watek.start()
        watki.append(watek)

    kolejka.join()

    for _ in watki:
        kolejka.put(None)

    for watek in watki:
        watek.join()

    print(f"\nLiczba odwiedzonych stron: {len(odwiedzone)}")
    print("Crawler zakończył pracę.")
