# Lekcja 36 – Zadanie 16

## Blue-Green Deployment

W zadaniu skonfigurowano i przetestowano wdrożenie aplikacji w modelu Blue-Green Deployment z wykorzystaniem Amazon EC2 Auto Scaling, Application Load Balancer oraz Target Group.

### Środowisko BLUE

Wykorzystano istniejącą grupę Auto Scaling:

Lesson13ASG

Konfiguracja:

- Min: 1
- Desired: 2
- Max: 3
- Launch Template: Lesson13ZeroDowntimeLT
- Launch Template Version: 4
- Target Group: lesson13-target-group
- Health check: /health

Instancje BLUE:

- i-02d962d439f82e22e
- i-0961d403fabcd6a65

Obie instancje były InService i Healthy.

### Przygotowanie GREEN

Utworzono nową wersję Launch Template:

- Launch Template: Lesson13ZeroDowntimeLT
- Version: 5
- Description: Lesson 16 GREEN version

Wersja GREEN uruchamia nginx i udostępnia stronę:

Lesson 16 - BLUE-GREEN DEPLOYMENT - GREEN VERSION

oraz endpoint health check:

/health

Utworzono nową grupę Auto Scaling:

Lesson16GreenASG

Konfiguracja:

- Min: 0
- Desired: 2
- Max: 2
- Launch Template Version: 5

Instancje GREEN:

- i-039a44efd62086f0c
- i-0a9e2f84f782b01d4

Obie instancje zostały uruchomione jako InService i Healthy.

### Health Check GREEN

Instancje GREEN zostały zarejestrowane w istniejącym Target Group:

lesson13-target-group

Obie instancje GREEN uzyskały status:

healthy

### Przełączenie BLUE → GREEN

Po potwierdzeniu poprawnego działania GREEN wyrejestrowano instancje BLUE z Target Group.

Instancje BLUE otrzymały status:

draining

Instancje GREEN pozostały:

healthy

Następnie przetestowano działanie aplikacji przez Application Load Balancer:

lesson13-alb

Test:

curl http://lesson13-alb-310374621.eu-central-1.elb.amazonaws.com/

Wynik:

Lesson 16 - BLUE-GREEN DEPLOYMENT - GREEN VERSION

Potwierdziło to prawidłowe przełączenie ruchu na GREEN.

### Rollback GREEN → BLUE

Następnie przeprowadzono test rollbacku.

Instancje BLUE zostały ponownie zarejestrowane w Target Group i uzyskały status:

healthy

Następnie wyrejestrowano instancje GREEN.

Instancje GREEN otrzymały status:

draining

Instancje BLUE pozostały:

healthy

Ponownie przetestowano aplikację przez ALB:

curl http://lesson13-alb-310374621.eu-central-1.elb.amazonaws.com/

Wynik:

Lesson 13 - ZERO DOWNTIME - VERSION 2

Potwierdziło to prawidłowy rollback z GREEN do BLUE.

### Wynik zadania

Przetestowano cały proces Blue-Green Deployment:

BLUE
↓
uruchomienie GREEN
↓
GREEN health check
↓
BLUE → GREEN
↓
test aplikacji przez ALB
↓
rollback GREEN → BLUE
↓
test aplikacji przez ALB

Pomyślnie zweryfikowano:

- uruchomienie GREEN,
- health check GREEN,
- przełączenie ruchu BLUE → GREEN,
- działanie aplikacji GREEN przez ALB,
- rollback GREEN → BLUE,
- ponowne działanie aplikacji BLUE przez ALB.

Zadanie wykonane i zweryfikowane.
