# Zadanie 12 – Automated Backup Script

## Cel zadania

Celem zadania było przygotowanie skryptu automatycznego backupu RDS,
który:

- tworzy codziennie snapshot RDS o godzinie 02:00,
- usuwa snapshoty starsze niż 7 dni,
- wysyła powiadomienie email po zakończeniu operacji,
- zapisuje wszystkie operacje do pliku logu.

## Implementacja

Skrypt znajduje się w:

`zadanie12/app.py`

Skrypt:

1. sprawdza dostępność instancji RDS,
2. tworzy manualny snapshot,
3. wyszukuje manualne snapshoty starsze niż 7 dni,
4. usuwa znalezione stare snapshoty,
5. zapisuje operacje do pliku `backup.log`,
6. wysyła powiadomienie email po zakończeniu operacji.

## Konfiguracja

Identyfikator instancji RDS można ustawić przez zmienną środowiskową:

```bash
export RDS_DB_IDENTIFIER="lesson36-postgres-db"
