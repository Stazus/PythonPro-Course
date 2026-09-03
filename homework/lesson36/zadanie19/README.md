# Lekcja 36 – Zadanie 19

## CloudWatch Monitoring, Custom Metrics, Alarms i SNS

Celem zadania było przygotowanie podstawowego monitoringu środowiska AWS
z wykorzystaniem Amazon CloudWatch, CloudWatch Logs, Custom Metrics,
CloudWatch Alarms oraz Amazon SNS.

### Środowisko

Wykorzystano istniejące środowisko AWS:

- Region: `eu-central-1`
- Auto Scaling Group: `Lesson13ASG`
- Launch Template: `Lesson13ZeroDowntimeLT`
- Application Load Balancer: `lesson13-alb`

### 1. CloudWatch Log Group

Utworzono grupę logów:

`/lesson19/application`

Ustawiono retencję:

`7 dni`

Utworzono również log stream:

`monitoring`

Weryfikacja potwierdziła:

- Log Group: `/lesson19/application`
- Retention: `7`

### 2. Amazon SNS

Utworzono topic SNS:

`Lesson19Monitoring`

ARN:

`arn:aws:sns:eu-central-1:672768959472:Lesson19Monitoring`

Topic został wykorzystany jako akcja alarmów CloudWatch.

### 3. Custom Metrics

Utworzono własne metryki CloudWatch w namespace:

`Lesson19/Application`

Wykorzystano metryki:

- `RequestRate`
- `ErrorRate`
- `Latency`

Wszystkie metryki wykorzystują wymiar:

`Application=Lesson13`

Przykładowe dane testowe:

- RequestRate: `25`
- ErrorRate: `10%`
- Latency: `3 s`

### 4. Alarm wysokiego CPU

Utworzono alarm:

`Lesson19-HighCPU`

Konfiguracja:

- Namespace: `AWS/EC2`
- Metric: `CPUUtilization`
- Statistic: `Average`
- Period: `300 s`
- Evaluation periods: `1`
- Threshold: `80`
- Operator: `GreaterThanThreshold`
- Dimension: `AutoScalingGroupName=Lesson13ASG`
- Alarm action: `Lesson19Monitoring`

Alarm został poprawnie utworzony.

Podczas późniejszej weryfikacji jego stan wynosił:

`OK`
### 5. Alarm wysokiego Error Rate

Utworzono alarm:

`Lesson19-HighErrorRate`

Konfiguracja:

- Namespace: `Lesson19/Application`
- Metric: `ErrorRate`
- Statistic: `Average`
- Period: `60 s`
- Evaluation periods: `1`
- Threshold: `5`
- Operator: `GreaterThanThreshold`
- Dimension: `Application=Lesson13`
- Alarm action: `Lesson19Monitoring`

#### Test alarmu

Wysłano do CloudWatch wartość:

`ErrorRate = 10%`

Próg alarmu wynosi:

`5%`

CloudWatch potwierdził przekroczenie progu.

Stan alarmu:

`ALARM`

Powód:

`Threshold Crossed: 1 datapoint [10.0] was greater than the threshold (5.0).`

Test potwierdził prawidłowe działanie alarmu.

### 6. Alarm wysokiego opóźnienia

Utworzono alarm:

`Lesson19-HighLatency`

Konfiguracja:

- Namespace: `Lesson19/Application`
- Metric: `Latency`
- Statistic: `Average`
- Period: `60 s`
- Evaluation periods: `1`
- Threshold: `2`
- Operator: `GreaterThanThreshold`
- Dimension: `Application=Lesson13`
- Alarm action: `Lesson19Monitoring`

#### Test alarmu

Wysłano do CloudWatch wartość:

`Latency = 3 s`

Próg alarmu wynosi:

`2 s`

CloudWatch potwierdził przekroczenie progu.

Stan alarmu:

`ALARM`

Powód:

`Threshold Crossed: 1 datapoint [3.0] was greater than the threshold (2.0).`

Test potwierdził prawidłowe działanie alarmu.

### 7. Wynik testów

Przeprowadzono testy własnych metryk oraz alarmów.

Wyniki:

| Alarm | Metric | Wartość testowa | Próg | Wynik |
|---|---|---:|---:|---|
| `Lesson19-HighCPU` | CPUUtilization | — | 80% | `OK` |
| `Lesson19-HighErrorRate` | ErrorRate | 10% | 5% | `ALARM` |
| `Lesson19-HighLatency` | Latency | 3 s | 2 s | `ALARM` |

Alarmy `ErrorRate` oraz `Latency` poprawnie przeszły do stanu `ALARM`
po przekroczeniu zdefiniowanych progów.

### 8. Architektura

Schemat monitoringu:

```text
                AWS Environment
                      |
          +-----------+-----------+
          |                       |
        EC2/ASG              Application
          |                    Metrics
          |                       |
          +-----------+-----------+
                      |
                 CloudWatch
                      |
          +-----------+-----------+
          |           |           |
       CPUAlarm   ErrorAlarm   LatencyAlarm
          |           |           |
          +-----------+-----------+
                      |
                     SNS
                      |
            Lesson19Monitoring

### Wynik zadania

Pomyślnie skonfigurowano podstawowy monitoring środowiska AWS.

Zweryfikowano:

- utworzenie CloudWatch Log Group,
- ustawienie retencji logów na 7 dni,
- utworzenie log stream,
- utworzenie SNS Topic,
- wysyłanie Custom Metrics,
- utworzenie alarmu CPU,
- utworzenie alarmu Error Rate,
- utworzenie alarmu Latency,
- prawidłowe przejście alarmu Error Rate do `ALARM`,
- prawidłowe przejście alarmu Latency do `ALARM`.

Zadanie wykonane i zweryfikowane.
