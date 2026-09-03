# Lekcja 36 – Zadanie 17

## CI/CD z GitHub Actions

Celem zadania jest przygotowanie kompletnego pipeline CI/CD obejmującego:

- testy unit,
- testy integracyjne,
- uruchamianie testów przy każdym push,
- automatyczny deployment do staging,
- health check staging,
- manual approval przed production,
- deployment do production,
- powiadomienia Slack,
- możliwość rollbacku.

### Środowiska

STAGING:

- `Lesson16GreenASG`
- Launch Template `Lesson13ZeroDowntimeLT`
- wersja GREEN

PRODUCTION:

- `Lesson13ASG`
- Launch Template `Lesson13ZeroDowntimeLT`
- wersja BLUE

### Status

Pipeline będzie rozwijany krok po kroku i testowany end-to-end.
