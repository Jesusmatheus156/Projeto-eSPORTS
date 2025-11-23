#!/usr/bin/env bash

# 1. Tenta criar o superusuário de forma não interativa.
# Depende das variáveis DJANGO_SUPERUSER_USERNAME e DJANGO_SUPERUSER_PASSWORD
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Criando superusuário com variáveis de ambiente..."
  # O '|| true' impede que o erro de usuário existente pare o deploy
  python manage.py createsuperuser --noinput || true
fi

# 2. Aplica as migrações no banco de dados.
echo "Aplicando migrações..."
python manage.py migrate --noinput

# 3. Coleta os arquivos estáticos (CSS/JS) para o WhiteNoise.
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# 4. Inicia o servidor Gunicorn.
echo "Iniciando Gunicorn..."
gunicorn projeto_eSports.wsgi --bind 0.0.0.0:10000