from pathlib import Path
import os
import dj_database_url

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

    'ckeditor',
    'ckeditor_uploader',

    # CLOUDINARY
    'cloudinary',
    'cloudinary_storage',
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
# ARQUIVOS ESTÁTICOS (STATIC)
# ---------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise serve os STATICFILES
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------------------
# MEDIA (AGORA NO CLOUDINARY)
# ---------------------------
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

# ---------------------------
# CKEDITOR
# ---------------------------
CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'

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
