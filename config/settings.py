import os
import environ
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# --- БАЗОВЫЕ ПУТИ ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- ИНИЦИАЛИЗАЦИЯ ENV ---
env = environ.Env()
# Читаем файл .env (убедись, что он лежит в корне проекта рядом с manage.py)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --- БЕЗОПАСНОСТЬ ---
# Берем ключ из .env. Если его там нет, вылетит ошибка (это правильно для безопасности)
SECRET_KEY = env('SECRET_KEY')

# Берем DEBUG из .env. Если не нашли — по умолчанию False
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ['qalzh.pythonanywhere.com', '127.0.0.1', 'localhost']

# --- ПРИЛОЖЕНИЯ ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Сторонние
    'rest_framework',
    
    # Твои приложения
    'shop',
    'account',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # Для смены языков
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.cart', # Твоя корзина
                'django.template.context_processors.i18n', # Контекст для i18n
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- БАЗА ДАННЫХ ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- ВАЛИДАЦИЯ ПАРОЛЕЙ ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# --- ИНТЕРНАЦИОНАЛИЗАЦИЯ (i18n) ---
LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('ru', _('Russian')),
    ('kk', _('Kazakh')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- СТАТИКА И МЕДИА ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# Папка, куда соберется вся статика после collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- НАСТРОЙКИ МАГАЗИНА ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
CART_SESSION_ID = 'cart'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

if not DEBUG:
    # Редирект с http на https
    SECURE_SSL_REDIRECT = True
    # Куки только через защищенное соединение
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS (строгое следование HTTPS)
    SECURE_HSTS_SECONDS = 31536000  # 1 год
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True