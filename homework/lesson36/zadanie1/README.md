# Zadanie 1 – Tworzenie RDS Instance

## Cel zadania

Celem zadania było napisanie skryptu w Pythonie z użyciem `boto3`, który:

- tworzy instancję RDS PostgreSQL,
- używa klasy `db.t3.micro`,
- ustawia backup retention na 3 dni,
- po utworzeniu instancji tworzy manualny snapshot.

## Implementacja

Skrypt znajduje się w:

`zadanie1/app.py`

Wykorzystuje:

- AWS SDK for Python (`boto3`),
- PostgreSQL,
- RDS,
- zmienną środowiskową `RDS_MASTER_PASSWORD` do bezpiecznego przekazania hasła.

Skrypt oczekuje na osiągnięcie przez instancję statusu `available`, a następnie tworzy manualny snapshot.

## Test

Najpierw sprawdzono uprawnienia użytkownika IAM:

```bash
aws rds describe-db-instances --region eu-central-1
