#!/bin/sh

echo "Czekam na PostgreSQL..."

until python -c "
import psycopg2
psycopg2.connect(
    dbname='appdb',
    user='appuser',
    password='apppassword',
    host='database',
    port='5432'
)
" 2>/dev/null
do
    echo "Baza jeszcze niedostępna..."
    sleep 2
done

echo "Baza dostępna."

echo "Uruchamiam migracje..."
python manage.py migrate

echo "Tworzę superusera, jeśli nie istnieje..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print('Superuser utworzony.')
else:
    print('Superuser już istnieje.')
"

echo "Inicjalizacja zakończona."
