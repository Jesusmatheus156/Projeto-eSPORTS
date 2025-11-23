"""
Django settings for projeto_eSports project.
"""

from pathlib import Path
import os
import dj_database_url # Importado para ler a URL do banco

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Use a variável de ambiente SECRET_KEY no Render para segurança
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-slqd-#1*$2(13^#!o7r9u*@gpuxdes1jck_2ecvbze-w040rnt')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True' # Lê a variável de ambiente DEBUG, False por padrão

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost', 
    'projeto-esports-4bzr.onrender.com', 
    '.render.com', 
    'reisdatorre.site', 
    'www.reisdatorre.site', 
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_eSports',
    
    # CKEditor e Uploads
    'ckeditor',
    'ckeditor_uploader', # Necessário para o recurso de upload do editor
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    # WhiteNoise deve vir ANTES de SessionMiddleware e CommonMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app_eSports.middleware.VisitCounterMiddleware',
    # A linha 'django.contrib.sessions.middleware.SessionMiddleware' duplicada foi removida
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

# A LÓGICA DE MIGRAÇÃO E COLLECTSTATIC FOI MOVIDA PARA o Start Command no Render
# ----------------------------------------------------

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# ----------------------------------------------------
## 📂 Static Files (CSS, JS, Images)
# ----------------------------------------------------

# URL base para arquivos estáticos
STATIC_URL = 'static/'

# Diretório de destino para 'python manage.py collectstatic'
STATIC_ROOT = BASE_DIR / 'staticfiles' 

# Configuração WhiteNoise para otimizar arquivos estáticos em produção
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 

# ----------------------------------------------------
## 🖼️ Media Files (User Uploads) & CKEditor
# ----------------------------------------------------

# URL para arquivos de mídia (uploads de usuário)
MEDIA_URL = '/media/'

# Diretório local para uploads (não persistente no Render sem S3/Cloud Storage)
MEDIA_ROOT = BASE_DIR / 'media'

# Configuração obrigatória do CKEditor para o caminho de upload
CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'

# Configuração opcional do CKEditor para personalizar a barra de ferramentas, etc.
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'