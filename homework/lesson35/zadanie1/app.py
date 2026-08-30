import time

import requests


urls = [
    "https://www.google.com",
    "https://www.python.org",
    "https://github.com",
]


for url in urls:
    try:
        start_time = time.time()

        response = requests.get(url, timeout=5)

        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            print(
                f"{url} - OK (200), "
                f"czas odpowiedzi: {elapsed_time:.2f} s"
            )
        else:
            print(
                f"{url} - status {response.status_code}, "
                f"czas odpowiedzi: {elapsed_time:.2f} s"
            )

    except requests.exceptions.RequestException as error:
        print(f"{url} - błąd połączenia: {error}")
