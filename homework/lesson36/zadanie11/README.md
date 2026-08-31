# Zadanie 11 – Weighted Routing Test

## Cel zadania

Celem zadania było przygotowanie weighted routing w Amazon Route53:

- 80% ruchu do endpointu primary,
- 20% ruchu do endpointu canary,
- wysłanie 100 requestów,
- policzenie, który endpoint otrzymał request.

Oczekiwany wynik to około 80/20.

## Implementacja

Skrypt znajduje się w:

`zadanie11/app.py`

Skrypt:

1. pobiera Hosted Zone ID z `ROUTE53_HOSTED_ZONE_ID`,
2. pobiera adres endpointu primary z `PRIMARY_ENDPOINT`,
3. pobiera adres endpointu canary z `CANARY_ENDPOINT`,
4. tworzy dwa rekordy Route53 typu A,
5. ustawia weighted routing:
   - primary: 80,
   - canary: 20,
6. wysyła 100 requestów do domeny,
7. rozpoznaje endpoint na podstawie nagłówka `X-Endpoint`,
8. zlicza odpowiedzi primary i canary,
9. wyświetla procentowy rozkład ruchu.

## Konfiguracja

Przykładowe zmienne środowiskowe:

```bash
export ROUTE53_HOSTED_ZONE_ID="ZXXXXXXXXXXXXX"
export ROUTE53_DOMAIN="test.yourdomain.com"
export PRIMARY_ENDPOINT="1.2.3.4"
export CANARY_ENDPOINT="5.6.7.8"
