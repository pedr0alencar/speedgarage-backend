"""
Django settings for speedgarage project.
Gerado pelo 'django-admin startproject'.

ATENÇÃO
-------------------------------------------
• Nunca exponha SECRET_KEY nem DEBUG=True em produção.
• Mantenha variáveis sensíveis no .env (ex.: DJANGO_SECRET_KEY, DATABASE_URL).
"""

from pathlib import Path
import os
from datetime import timedelta

# ------------------------------------------------------------------
# Caminhos
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Variáveis de ambiente básicas
# ------------------------------------------------------------------
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'unsafe-dev-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # domínio Railway/Vercel em produção, ex.:
    # 'speedgarage-production.up.railway.app',
]

# ------------------------------------------------------------------
# Aplicações
# ------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceiros
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    # apps
    'reviews',
]

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',          #  ← precisa vir antes do CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------------
# URLs / WSGI
# ------------------------------------------------------------------
ROOT_URLCONF = 'speedgarage.urls'
WSGI_APPLICATION = 'speedgarage.wsgi.application'

# ------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------------------------------------------
# Banco de dados (SQLite DEV → PostgreSQL PROD via DATABASE_URL)
# ------------------------------------------------------------------
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

# ------------------------------------------------------------------
# Usuario customizado (se usar o modelo Usuario em reviews)
# ------------------------------------------------------------------
# AUTH_USER_MODEL = 'reviews.Usuario'

# ------------------------------------------------------------------
# Validação de senha (padrão Django)
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------------
# Internacionalização
# ------------------------------------------------------------------
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Arquivos estáticos
# ------------------------------------------------------------------
STATIC_URL = 'static/'

# ------------------------------------------------------------------
# REST Framework + JWT
# ------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# ------------------------------------------------------------------
# CORS
# ------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',      # Angular dev
]

# ------------------------------------------------------------------
# Chave primária padrão
# ------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
