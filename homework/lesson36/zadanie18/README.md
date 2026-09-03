# Lekcja 36 – Zadanie 18

## Scheduled Scaling i zarządzanie środowiskiem AWS

W zadaniu skonfigurowano automatyczne skalowanie grupy Auto Scaling z wykorzystaniem Scheduled Actions.

### Środowisko

Wykorzystano grupę Auto Scaling:

Lesson16GreenASG

Grupa GREEN została wykorzystana jako środowisko nieprodukcyjne.

### Konfiguracja

- Min: 0
- Desired: 2
- Max: 2
- Launch Template: Lesson13ZeroDowntimeLT
- Launch Template Version: 5

### Scheduled Scaling

Utworzono dwie zaplanowane akcje Auto Scaling.

### Scale Down – noc

Nazwa:

Lesson18ScaleDownNight

Harmonogram:

0 22 * * *

Codziennie o 22:00 UTC grupa jest ustawiana na:

- Min: 0
- Desired: 0
- Max: 2

Celem jest ograniczenie kosztów środowiska GREEN poza godzinami pracy.

### Scale Up – rano

Nazwa:

Lesson18ScaleUpMorning

Harmonogram:

0 5 * * *

Codziennie o 05:00 UTC grupa jest ustawiana na:

- Min: 0
- Desired: 2
- Max: 2

Celem jest automatyczne uruchomienie środowiska GREEN rano.

### Weryfikacja

Utworzone Scheduled Actions zostały sprawdzone poleceniem:

aws autoscaling describe-scheduled-actions --auto-scaling-group-name Lesson16GreenASG --region eu-central-1

Potwierdzono utworzenie:

- Lesson18ScaleDownNight → 0 22 * * * → Desired 0
- Lesson18ScaleUpMorning → 0 5 * * * → Desired 2

### Wynik

Scheduled Scaling zostało poprawnie skonfigurowane dla środowiska GREEN.

Mechanizm umożliwia automatyczne ograniczenie liczby instancji poza godzinami pracy oraz ponowne uruchomienie środowiska rano.

Zadanie wykonane i zweryfikowane.
