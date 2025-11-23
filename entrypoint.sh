#!/usr/bin/env bash

echo "Aplicando migrações..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Criando superusuário..."
python manage.py createsuperuser --noinput || true

echo "Iniciando Gunicorn..."
gunicorn projeto_eSports.wsgi:application --bind 0.0.0.0:$PORT
