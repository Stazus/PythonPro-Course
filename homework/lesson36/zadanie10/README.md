# Zadanie 10 – Application Load Balancer Setup

## Cel zadania

Celem zadania było przygotowanie kompletnej konfiguracji
Application Load Balancer (ALB), która:

- wykorzystuje dwa subnety,
- posiada Target Group z health checkiem,
- posiada Listener HTTP na porcie 80,
- rejestruje dwie instancje EC2,
- umożliwia testowanie rozdzielania ruchu pomiędzy instancje.

## Implementacja

Skrypt znajduje się w:

`zadanie10/app.py`

Skrypt:

1. pobiera identyfikatory dwóch instancji EC2 ze zmiennej
   `EC2_INSTANCE_IDS`,
2. wyszukuje domyślne VPC,
3. wybiera dwa subnety znajdujące się w różnych Availability Zones,
4. tworzy Security Group dla ALB,
5. tworzy Target Group,
6. konfiguruje health check HTTP na `/health`,
7. tworzy Application Load Balancer,
8. rejestruje dwie instancje EC2 w Target Group,
9. tworzy Listener HTTP na porcie 80,
10. wyświetla adres DNS ALB.

### Parametry

- region: `eu-central-1`
- Target Group port: `8000`
- Listener port: `80`
- health check: `/health`
- protokół: HTTP
- typ load balancera: Application Load Balancer
- schemat: internet-facing

## Konfiguracja instancji

Identyfikatory dwóch instancji są przekazywane przez zmienną środowiskową:

```bash
export EC2_INSTANCE_IDS="i-xxxxxxxx,i-yyyyyyyy"
