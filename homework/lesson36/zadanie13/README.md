# Lekcja 36 – Zadanie 13
## Zero Downtime Deployment

Celem zadania było przygotowanie wdrożenia aplikacji na AWS z wykorzystaniem
Auto Scaling Group oraz Application Load Balancer.

### Wykorzystane elementy

- Amazon EC2
- Launch Template
- Auto Scaling Group
- Application Load Balancer
- Target Group
- Health Check
- Instance Refresh
- Rolling Update

### Konfiguracja

Region:

`eu-central-1`

Launch Template:

`Lesson13ZeroDowntimeLT`

Wersja użyta podczas wdrożenia:

`4`

AMI:

`ami-0f2f6d6f49dbe9fd1`

Typ instancji:

`t3.micro`

Auto Scaling Group:

`Lesson13ASG`

Desired / Min / Max:

`2 / 2 / 2`

Target Group:

`lesson13-target-group`

Health Check:

`HTTP /health`

### Test

Application Load Balancer:

`lesson13-alb`

Podczas Instance Refresh wykonano rolling update z wersji 3 do wersji 4
Launch Template.

W trakcie aktualizacji ALB cały czas odpowiadał na żądania HTTP.

Zaobserwowano odpowiedzi zarówno starej, jak i nowej wersji aplikacji:

- `Lesson 13 - Zero Downtime Deployment`
- `Lesson 13 - ZERO DOWNTIME - VERSION 2`

Target Group po zakończeniu aktualizacji zawierała 2 zdrowe instancje.

Końcowy status Instance Refresh:

`Successful`

Postęp:

`100%`

Wynik potwierdza wykonanie rolling update bez przerwy w dostępności
aplikacji przez ALB.
