# settings.py

from pathlib import Path
import os
import dj_database_url
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-slqd-#1*$2(13^#!o7r9u*@gpuxdes1jck_2ecvbze-w040rnt'
)

DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.render.com',
    'projeto-esports-4bzr.onrender.com',
    'reisdatorre.site',
    'www.reisdatorre.site',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app_eSports',

    # CLOUDINARY (Antes de ckeditor_uploader, se este for usar storage)
    'cloudinary',
    'cloudinary_storage',

    'ckeditor',
    'ckeditor_uploader', # Deve vir DEPOIS de cloudinary_storage, se for o caso
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WHITENOISE PARA STATICFILES
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'app_eSports.middleware.VisitCounterMiddleware',
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

# ---------------------------
# BANCO DE DADOS
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

# ---------------------------
# VALIDADORES
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ---------------------------
# 1. ARQUIVOS ESTÁTICOS (STATIC) - Otimizado
# ---------------------------
# No Render, é melhor deixar o WhiteNoise gerenciar os arquivos estáticos
# (CSS, JS) e o Cloudinary gerenciar apenas os arquivos de MÍDIA (uploads).
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise serve os STATICFILES
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ---------------------------
# 2. MEDIA (AGORA NO CLOUDINARY) - Correção para o Storage
# ---------------------------
# Isto garante que os uploads de ImageField e FileField vão para o Cloudinary.
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/' # Mantido, mas não será usado pelo Cloudinary diretamente

# ---------------------------
# 3. CKEDITOR - Correção para uploads de imagens embutidas
# ---------------------------
CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'

# CRÍTICO: Define o Cloudinary como o backend para o upload de imagens do CKEditor
CKEDITOR_IMAGE_BACKEND = 'cloudinary_storage.backends.CloudinaryBackend'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    }
}

# ---------------------------
# SUPERUSER AUTOMÁTICO
# ---------------------------
DJANGO_SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------
# 4. CONFIGURAÇÃO CLOUDINARY - Ajuste: Remover bloco desnecessário
# ---------------------------
# Se você definir as variáveis de ambiente CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY
# e CLOUDINARY_API_SECRET no Render, o 'django-cloudinary-storage' e o próprio
# SDK já as pegam automaticamente. Este bloco não é necessário e pode ser removido
# ou usado como fallback. Vou comentar para clareza, mas mantê-lo é inofensivo
# se você garantir que as variáveis de ambiente estão configuradas.

# cloudinary.config( 
#   cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'), 
#   api_key = os.environ.get('CLOUDINARY_API_KEY'), 
#   api_secret = os.environ.get('CLOUDINARY_API_SECRET') 
# )