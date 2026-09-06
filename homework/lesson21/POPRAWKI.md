# Lekcja 21 – poprawki po uwagach mentora

## Zadanie 4 – Plik statyczny CSS

Mentor zgłosił uwagę, że w kodzie brakowało pliku `style.css`, mimo że jego podłączenie w szablonie zostało wykonane.

Plik `style.css` znajduje się obecnie w repozytorium pod ścieżką:

`notatnik/static/notatnik/style.css`

Plik zawiera wymaganą w zadaniu regułę:

```css
body {
    background-color: #f0f8ff;
}
```

Plik CSS jest prawidłowo podłączony w szablonie:

`templates/category_list.html`

za pomocą:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'notatnik/style.css' %}">
```

Plik `style.css` został dodany do historii repozytorium w commicie:

`d1540de Dodano task4_style_css`

W obecnym stanie repozytorium Zadanie 4 zawiera więc zarówno plik CSS, jak i jego podłączenie w szablonie.


## Zadanie 8 – Logika warunkowa „NOWOŚĆ!”

Mentor zgłosił, że napis `NOWOŚĆ!` był wyświetlany dla każdego artykułu posiadającego datę utworzenia, zamiast tylko dla artykułów z ostatnich 3 dni.

Poprzedni warunek w szablonie sprawdzał jedynie istnienie daty `created_at`.

Poprawiono logikę poprzez obliczenie w widoku daty granicznej sprzed 3 dni:

```python
from datetime import timedelta
from django.utils import timezone

three_days_ago = timezone.now() - timedelta(days=3)
```

Wartość `three_days_ago` jest przekazywana do szablonu:

```python
{
    "articles": articles,
    "q": q,
    "three_days_ago": three_days_ago,
}
```

W szablonie `templates/article_list.html` napis `NOWOŚĆ!` jest teraz wyświetlany tylko dla artykułów utworzonych w ciągu ostatnich 3 dni:

```django
{% if article.created_at >= three_days_ago %}
    <strong>NOWOŚĆ!</strong>
{% endif %}
```

Jednocześnie widok nadal pobiera wyłącznie artykuły opublikowane:

```python
articles = Article.objects.filter(
    is_published=True
)
```

Poprawka Zadania 8 została zapisana w commicie:

`3d0fb96 Lekcja 21 - poprawka zadania 8`

Po wprowadzeniu zmian wykonano sprawdzenie projektu poleceniem:

```bash
python manage.py check
```

Wynik:

```text
System check identified no issues (0 silenced).
```

Uruchomiono również:

```bash
python manage.py test
```

Projekt nie zawiera obecnie testów automatycznych dla tej lekcji (`Found 0 test(s)`), ale kontrola systemowa Django nie wykazała żadnych błędów.
