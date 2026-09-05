# Zadanie 20 – Full-stack app z AI

Aplikacja full-stack rekomendująca książki na podstawie preferencji użytkownika.

## Technologie

- React + Vite – frontend
- Nginx – serwowanie frontendu i proxy do API
- FastAPI – backend REST API
- PostgreSQL – historia rekomendacji
- Redis – cache oraz broker dla Celery
- Celery – asynchroniczne wykonywanie zadań AI
- Ollama – lokalne AI
- nomic-embed-text – model do tworzenia embeddingów
- Docker Compose – uruchamianie całego środowiska

## Jak działa aplikacja

Użytkownik wpisuje opis książek lub gatunków, które lubi.

Backend przekazuje zadanie do Celery. Model `nomic-embed-text`
uruchomiony lokalnie przez Ollamę tworzy embedding preferencji
użytkownika oraz opisów książek.

Aplikacja oblicza podobieństwo cosinusowe i zwraca trzy najlepiej
dopasowane książki.

Wynik jest zapisywany w PostgreSQL oraz przez godzinę przechowywany
w cache Redis.

## Uruchomienie

Najpierw uruchom Ollamę:

```bash
docker compose up -d ollama
```

Pobierz model embeddingowy:

```bash
docker compose exec ollama ollama pull nomic-embed-text
```

Uruchom aplikację:

```bash
docker compose up --build
```

Frontend jest dostępny pod adresem:

```text
http://localhost:8080
```

## AI

W zadaniu wykorzystano dopuszczony lokalny wariant Ollama zamiast
zewnętrznego API OpenAI. Dzięki temu aplikacja nie wymaga klucza API
ani płatnego dostępu do zewnętrznej usługi.
