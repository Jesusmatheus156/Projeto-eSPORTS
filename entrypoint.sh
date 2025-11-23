#!/usr/bin/env bash

echo "=========================================="
echo "  Iniciando Script de Deploy do Render    "
echo "=========================================="

# 1. Aplicar Migrações do Banco de Dados
echo "Aplicando Migrações (python manage.py migrate)..."
python manage.py migrate --noinput

# 2. Coletar Arquivos Estáticos
echo "Coletando Arquivos Estáticos (python manage.py collectstatic)..."
python manage.py collectstatic --noinput

# 3. Criar Superusuário (OPCIONAL: Use se precisar de um usuário inicial via V.E.)
# Este comando só funciona se as Variáveis de Ambiente DJANGO_SUPERUSER_...
# estiverem definidas no Render.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  echo "Verificando e Criando Superusuário..."
  python manage.py createsuperuser --noinput || true
fi

# 4. Iniciar o Servidor Gunicorn
echo "Iniciando Gunicorn..."
# O --bind 0.0.0.0:10000 é crucial para o Render
gunicorn projeto_eSports.wsgi --bind 0.0.0.0:10000