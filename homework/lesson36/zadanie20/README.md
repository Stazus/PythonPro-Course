# Lekcja 36 – Zadanie 20

## Budowa infrastruktury sieciowej AWS

Celem zadania jest przygotowanie wielostrefowej infrastruktury sieciowej
w AWS z wykorzystaniem VPC, publicznych i prywatnych subnetów,
Internet Gateway, NAT Gateway oraz routingu.

### Środowisko

- Region: `eu-central-1`
- VPC: `vpc-069b5dde967f7b442`
- CIDR VPC: `172.31.0.0/16`

W zadaniu wykorzystano istniejącą VPC z poprzednich lekcji.

### Availability Zones

Wykorzystano trzy Availability Zones:

- `eu-central-1a`
- `eu-central-1b`
- `eu-central-1c`

### Publiczne subnety

W istniejącej VPC znajdują się trzy publiczne subnety:

- `172.31.0.0/20` → `eu-central-1c`
- `172.31.16.0/20` → `eu-central-1a`
- `172.31.32.0/20` → `eu-central-1b`

Publiczne subnety mają:

`MapPublicIpOnLaunch = True`

### Prywatne subnety

Utworzono trzy prywatne subnety:

- `172.31.48.0/20` → `eu-central-1a`
- `172.31.64.0/20` → `eu-central-1b`
- `172.31.80.0/20` → `eu-central-1c`

Subnety:

- `subnet-05b9cad72ba6ca0d8`
- `subnet-0d284396891692b5e`
- `subnet-0628640f9a83d0692`

Wszystkie prywatne subnety mają:

`MapPublicIpOnLaunch = False`

### Internet Gateway

Wykorzystano istniejący Internet Gateway:

`igw-073592ae07ea29869`

Jest on podłączony do VPC:

`vpc-069b5dde967f7b442`

### Prywatna Route Table

Utworzono prywatną tabelę routingu:

`rtb-0ae8172381ae37a5d`

Do tabeli przypisano wszystkie trzy prywatne subnety.

Tabela zawiera trasy:

`172.31.0.0/16 → local`

`0.0.0.0/0 → NAT Gateway`

### NAT Gateway

Utworzono publiczny NAT Gateway:

- NAT Gateway ID: `nat-0d7d3820cc8cc5f9b`
- State: `available`
- Public IP: `63.187.238.135`
- Elastic IP Allocation ID: `eipalloc-0873cb56478dfe61b`
- Public subnet: `subnet-03472013c9113da38`
- Availability Zone: `eu-central-1a`

NAT Gateway znajduje się w publicznym subnecie i zapewnia
prywatnym subnetom możliwość wychodzenia do Internetu.

### Routing prywatnej sieci

Do prywatnej Route Table dodano trasę:

`0.0.0.0/0 → nat-0d7d3820cc8cc5f9b`

Trasa ma stan:

`active`

Dzięki temu ruch z prywatnych subnetów kierowany do Internetu
jest przesyłany przez NAT Gateway.

Prywatne subnety nie otrzymują bezpośrednich publicznych adresów IP.

### Weryfikacja

Zweryfikowano poprawność konfiguracji:

- trzy publiczne subnety,
- trzy prywatne subnety,
- trzy Availability Zones,
- Internet Gateway,
- prywatną Route Table,
- NAT Gateway,
- trasę `0.0.0.0/0` przez NAT Gateway.

### Architektura

```text
                         Internet
                            |
                            |
                    Internet Gateway
                            |
              +-------------+-------------+
              |                           |
       Public Subnets              NAT Gateway
              |                           |
              |                    Private Route Table
              |                           |
              |              +------------+------------+
              |              |            |            |
              |           Private      Private      Private
              |           Subnet A     Subnet B     Subnet C
              |              |            |            |
              |           AZ-1a        AZ-1b        AZ-1c
              |
          AZ-1a / AZ-1b / AZ-1c

```

### Podsumowanie

W ramach zadania przygotowano wielostrefową infrastrukturę sieciową
w istniejącej VPC.

Utworzono:

- trzy prywatne subnety,
- prywatną Route Table,
- trzy przypisania subnetów do prywatnej Route Table,
- Elastic IP,
- NAT Gateway,
- trasę domyślną `0.0.0.0/0` przez NAT Gateway.

Wykorzystano istniejące zasoby:

- VPC,
- Internet Gateway,
- trzy publiczne subnety,
- trzy Availability Zones.

Prywatne subnety nie mają automatycznego przydzielania publicznych adresów IP,
a dostęp do Internetu realizują przez NAT Gateway.

Konfiguracja została zweryfikowana za pomocą AWS CLI.

### Wynik zadania

Infrastruktura sieciowa została poprawnie skonfigurowana i zweryfikowana.

Zadanie wykonane i zweryfikowane.
