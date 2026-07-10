"""
Django settings for core project.
"""

from pathlib import Path
import os  # ← این رو اضافه کن

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-c19l9b%cyx)&s6r!shx@#x*j5qu#q)ndl5&*t6lw=dx)-)wg2t'
DEBUG = False
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.onrender.com',
    'auratalkchat.onrender.com',
    'https://auratalk.com',
]

# ===== CSRF Trusted Origins (برای جلوگیری از خطای 403) =====
CSRF_TRUSTED_ORIGINS = [
    'https://auratalkchat.onrender.com',
    'http://auratalkchat.onrender.com',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'channels',
    'aura',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================
# تنظیمات فایل‌های استاتیک (STATIC)
# ============================================
STATIC_URL = '/static/'  # ← حتماً با / شروع بشه
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ← جایی که collectstatic فایل‌ها رو جمع می‌کنه
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # ← جایی که فایل‌های استاتیک خودت رو می‌ذاری
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===== تنظیمات Channels و WebSocket =====
ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    },
}

# ===== تنظیمات فایل =====
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB

