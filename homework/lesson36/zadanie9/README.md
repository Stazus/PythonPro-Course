# Zadanie 9 – Multi-AZ RDS z Failover

## Cel zadania

Celem zadania było przygotowanie rozwiązania, które:

- tworzy instancję RDS PostgreSQL w trybie Multi-AZ,
- testuje połączenie z bazą,
- wykonuje failover,
- mierzy czas niedostępności podczas failover,
- wyświetla raport z wynikiem pomiaru.

## Implementacja

Skrypt znajduje się w:

`zadanie9/app.py`

Instancja RDS jest konfigurowana jako:

- silnik: PostgreSQL,
- klasa: `db.t3.micro`,
- region: `eu-central-1`,
- Multi-AZ: `True`.

Skrypt pobiera endpoint instancji, wykonuje test połączenia,
uruchamia failover za pomocą `reboot_db_instance()` z parametrem
`ForceFailover=True`, a następnie mierzy czas od rozpoczęcia
niedostępności do ponownego uzyskania połączenia.

## Ograniczenie wykonania w AWS

Kod został przygotowany zgodnie z treścią zadania.

Test na rzeczywistej instancji Multi-AZ nie został wykonany na koncie AWS,
ponieważ konto posiada ograniczenia Free Tier. Wcześniejsza próba utworzenia
wymaganej instancji RDS zakończyła się błędem:

`FreeTierRestrictionError`

W związku z tym nie wykonywano rzeczywistego failoveru, aby nie generować
niekontrolowanych kosztów AWS.

## Weryfikacja kodu

Kod został sprawdzony poleceniem:

```bash
python -m py_compile zadanie9/app.py
