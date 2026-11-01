"""
Django settings for config project.
"""

import os
from pathlib import Path
from datetime import timedelta

import cloudinary                     
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# الأمان الأساسي
# ============================================================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-r@%-woi1zq(%x28k-lv+a$!95r%()6vp_p$ul_yq31(=j7)d_f'
)

DEBUG = os.environ.get('DEBUG', 'False') == 'True'


# ============================================================
# المضيفون المسموح لهم
# ============================================================

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# ============================================================
# التطبيقات
# ============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',   
    'cloudinary',

    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',

    # Local apps
    'core',
    'academics',
    'news',
    'careers',
    'admissions',
    'services',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # يجب أن يبقى أولًا
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# ============================================================
# قاعدة البيانات
# ============================================================

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': {
            **dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
                ssl_require=True,
            ),
            'DISABLE_SERVER_SIDE_CURSORS': True,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ============================================================
# كلمات المرور
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================================
# التدويل
# ============================================================

LANGUAGE_CODE = 'ar-sa'
TIME_ZONE = 'Asia/Damascus'
USE_I18N = True
USE_TZ = True


# ============================================================
# الملفات الثابتة والوسائط
# ============================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')   # يبقى للتطوير المحلي فقط

# ✅ NEW — بيانات اعتماد Cloudinary (تُقرأ من متغيرات البيئة)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY':    os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# ✅ NEW — ربط مكتبة Cloudinary الأساسية
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
)

# ✅ CHANGED — استخدام Cloudinary للوسائط في الإنتاج، والقرص المحلي في التطوير
if DEBUG:
    _media_backend = "django.core.files.storage.FileSystemStorage"
else:
    _media_backend = "cloudinary_storage.storage.MediaCloudinaryStorage"

STORAGES = {
    "default": {
        "BACKEND": _media_backend,
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# Django REST Framework
# ============================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}


# ============================================================
# Simple JWT
# ============================================================

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# ============================================================
# CORS — دعم عدة نطاقات (الموقع العام + لوحة التحكم + غيرها)
# ============================================================

_FALLBACK_ORIGINS = [
    'https://future-private-university.onrender.com',
]

def _parse_origins(raw: str) -> list[str]:
    return [o.strip().rstrip('/') for o in raw.split(',') if o.strip()]


if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = []
else:
    CORS_ALLOW_ALL_ORIGINS = False

    _env_urls = _parse_origins(os.environ.get('FRONTEND_URLS', ''))
    _legacy_url = os.environ.get('FRONTEND_URL', '').strip().rstrip('/')

    CORS_ALLOWED_ORIGINS = list(dict.fromkeys(
        _env_urls
        + ([_legacy_url] if _legacy_url else [])
        + _FALLBACK_ORIGINS
    ))


# ============================================================
# CSRF Trusted Origins — دعم عدة نطاقات
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:8001',
    'http://127.0.0.1:8001',
    'http://localhost:3000',
    'http://localhost:5173',
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

CSRF_TRUSTED_ORIGINS += CORS_ALLOWED_ORIGINS
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS))


# ============================================================
# إعدادات أمان إضافية (تعمل فقط في الإنتاج)
# ============================================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'