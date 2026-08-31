# Zadanie 8 – Read Replica RDS

## Cel zadania

Celem zadania było napisanie skryptu w Pythonie z użyciem `boto3`, który:

- tworzy Read Replica dla istniejącej instancji RDS,
- wykorzystuje bazę `lesson36-postgres-db` jako źródło,
- tworzy replikę `lesson36-postgres-replica`,
- czeka na uzyskanie przez replikę statusu `available`,
- pobiera i wyświetla endpoint Read Replica.

## Implementacja

Skrypt znajduje się w:

`zadanie8/app.py`

Do utworzenia repliki wykorzystywana jest metoda:

`create_db_instance_read_replica()`

Parametry:

- region: `eu-central-1`
- baza źródłowa: `lesson36-postgres-db`
- replika: `lesson36-postgres-replica`
- klasa instancji: `db.t3.micro`
- dostęp publiczny: wyłączony

Po utworzeniu repliki skrypt wykorzystuje waiter
`db_instance_available`, a następnie pobiera endpoint za pomocą
`describe_db_instances`.

## Ograniczenie wykonania w AWS

Kod został przygotowany zgodnie z wymaganiami zadania.

Wykonanie zadania na koncie AWS nie było możliwe, ponieważ w momencie realizacji
zadania nie była dostępna instancja źródłowa `lesson36-postgres-db`.

Próba ponownego utworzenia instancji z Zadania 1 zakończyła się komunikatem
`FreeTierRestrictionError`, ponieważ konfiguracja wymagana w Zadaniu 1
(`BackupRetentionPeriod=3`) przekracza ograniczenia konta Free Tier.

W związku z tym Read Replica nie została utworzona na koncie AWS.

## Weryfikacja kodu

Kod został sprawdzony poleceniem:

```bash
python -m py_compile zadanie8/app.py
