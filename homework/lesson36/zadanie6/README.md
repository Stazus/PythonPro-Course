# Zadanie 6 – Route53 A Record

## Cel zadania

Utworzenie rekordu A w Amazon Route53:

- nazwa: `test.yourdomain.com`
- typ: `A`
- adres IP: `1.2.3.4`
- TTL: `300` sekund

## Implementacja

Skrypt `app.py` wykorzystuje bibliotekę `boto3` i operację
`change_resource_record_sets` do utworzenia lub aktualizacji rekordu DNS.

Identyfikator Hosted Zone jest pobierany ze zmiennej środowiskowej:

`ROUTE53_HOSTED_ZONE_ID`

## Wynik

Skrypt został poprawnie skompilowany i uruchomiony.

Konto AWS nie posiada Hosted Zone dla `yourdomain.com`, dlatego
nie utworzono rzeczywistego rekordu DNS.

Nie tworzono Hosted Zone tylko na potrzeby ćwiczenia.

## Wymagania rekordu

```text
Name:  test.yourdomain.com
Type:  A
Value: 1.2.3.4
TTL:   300
