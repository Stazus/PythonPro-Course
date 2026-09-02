# Lekcja 36 – Zadanie 15

## Custom Metric i Auto Scaling

Skonfigurowano automatyczne skalowanie grupy `Lesson13ASG` na podstawie własnej metryki CloudWatch `ActiveConnections`.

### Custom Metric

- Namespace: `Lesson15/Application`
- Metric: `ActiveConnections`
- Unit: `Count`
- Dimension: `AutoScalingGroupName=Lesson13ASG`

### Auto Scaling

Zakres grupy:

- Min: 1
- Desired: 2
- Max: 3

Utworzono polityki:

- `Lesson15ScaleOut` → +1 instancja
- `Lesson15ScaleIn` → -1 instancja

### CloudWatch Alarms

- `Lesson15-ScaleOut` — `ActiveConnections > 100` → +1 instancja
- `Lesson15-ScaleIn` — `ActiveConnections < 20` → -1 instancja

### Test

Scale Out:

`ActiveConnections = 101`

Rezultat:

`2 → 3 instancje`

Scale In:

`ActiveConnections = 10`

Rezultat:

`3 → 2 instancje`

Oba mechanizmy skalowania zostały pomyślnie przetestowane.

Zadanie wykonane i zweryfikowane.
