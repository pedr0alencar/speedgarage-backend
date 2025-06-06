"""
Django settings para speedgarage.

Gerado pelo 'django-admin startproject'.

ATENÇÃO
-------------------------------------------
• Nunca exponha SECRET_KEY nem DEBUG=True em produção.
• Mantenha variáveis sensíveis em variáveis de ambiente (ex.: DJANGO_SECRET_KEY, DATABASE_URL).
"""

import os
from pathlib import Path
from datetime import timedelta
import dj_database_url

# ------------------------------------------------------------------
# Caminhos
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Variáveis de ambiente básicas
# ------------------------------------------------------------------
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'unsafe-dev-key'
)

DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Em produção, defina DJANGO_ALLOWED_HOSTS="dominio1.com,dominio2.com"
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ------------------------------------------------------------------
# Aplicações instaladas
# ------------------------------------------------------------------
INSTALLED_APPS = [
    # Core do Django
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

    # Apps do projeto
    'reviews',
]

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',       # ← Serve arquivos estáticos em produção
    'corsheaders.middleware.CorsMiddleware',            # ← Deve vir antes de CommonMiddleware
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
# Banco de dados (SQLite para DEV → PostgreSQL via DATABASE_URL em PROD)
# ------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        ssl_require=False
    )
}

# ------------------------------------------------------------------
# Modelo de usuário customizado (se for usar)
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
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# WhiteNoise já está configurado no MIDDLEWARE para servir estes arquivos

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
    'http://localhost:4200',      # Angular em dev
    # Em produção, adicione o domínio do front (por ex.: 'https://meu-frontend.vercel.app')
]

# ------------------------------------------------------------------
# Chave primária padrão
# ------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
