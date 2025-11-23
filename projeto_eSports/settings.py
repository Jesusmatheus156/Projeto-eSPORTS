"""
Django settings for projeto_eSports project.
...
"""

from pathlib import Path
import os
import dj_database_url # <--- IMPORT NOVO: Necessário para ler a URL do banco

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-slqd-#1*$2(13^#!o7r9u*@gpuxdes1jck_2ecvbze-w040rnt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # Mantenha como True para desenvolvimento local
# Mantenha como False para produção

ALLOWED_HOSTS = [
    '127.0.0.1', # Permite acesso pelo IP padrão local (solução para o traceback)
    'localhost', # Permite acesso pelo nome padrão (opcional, mas recomendado)

    '.render.com', # Permite todos os subdomínios do Render
    'reisdatorre.site', # Seu domínio
    'www.reisdatorre.site', # Seu subdomínio www
]

# Application definition
# ... (Restante do INSTALLED_APPS, MIDDLEWARE, ROOT_URLCONF, TEMPLATES, WSGI_APPLICATION permanece o mesmo) ...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_eSports',
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app_eSports.middleware.VisitCounterMiddleware', # <-- NOVA LINHA
]

ROOT_URLCONF = 'projeto_eSports.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app_eSports.context_processors.site_stats',
                'app_eSports.context_processors.live_status_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'projeto_eSports.wsgi.application'


# ----------------------------------------------------
## 🔄 Database
# ----------------------------------------------------

# Configuração Padrão (SQLite) - Usada se DATABASE_URL não estiver definida
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuração de Produção (PostgreSQL) - Prioriza a variável de ambiente do Render
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        ssl_require=True, # Importante para conexão segura com o Render
        default=os.environ.get('DATABASE_URL')
    )
    # Garante o engine correto no Render
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

# ----------------------------------------------------
# ... (Restante das configurações permanece o mesmo) ...

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
# ... (auth validators permanecem o mesmo) ...
]


# Internationalization
# ... (LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ permanecem o mesmo) ...

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# ... (STATIC_URL, DEFAULT_AUTO_FIELD permanecem o mesmo) ...

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configuração de arquivos de Mídia (Uploads de usuário)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
CKEDITOR_UPLOAD_PATH = 'uploads/'
