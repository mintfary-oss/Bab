"""Настройки Django для проекта BabyBlog."""

import os
from pathlib import Path

import environ

# ─── Базовые пути ───
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Переменные окружения ───
env = environ.Env(
    DJANGO_DEBUG=(bool, True),
    DJANGO_ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1", "0.0.0.0"]),
    POSTGRES_DB=(str, "babyblog"),
    POSTGRES_USER=(str, "babyblog"),
    POSTGRES_PASSWORD=(str, "babyblog_secret"),
    POSTGRES_HOST=(str, "db"),
    POSTGRES_PORT=(int, 5432),
    REDIS_URL=(str, "redis://redis:6379/0"),
    EMAIL_HOST=(str, "mailhog"),
    EMAIL_PORT=(int, 1025),
    EMAIL_USE_TLS=(bool, False),
    DEFAULT_FROM_EMAIL=(str, "noreply@babyblog.local"),
    MAX_IMAGE_SIZE_MB=(int, 10),
    MAX_VIDEO_SIZE_MB=(int, 200),
    MAX_DOCUMENT_SIZE_MB=(int, 50),
)

# Ищем .env в нескольких местах (Docker и локальный запуск)
for env_path in [
    BASE_DIR / ".env",           # app/.env
    BASE_DIR.parent / ".env",    # project_root/.env
    Path("/app/.env"),           # Docker fallback
]:
    if env_path.exists():
        environ.Env.read_env(str(env_path))
        break

# ─── Безопасность ───
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "insecure-dev-key-change-in-production"
)
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["http://localhost", "http://127.0.0.1"],  # type: ignore[call-overload]
)

# ─── Приложения ───
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # Сторонние
    "rest_framework",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_celery_beat",
    "django_cleanup.apps.CleanupConfig",
    # Приложения проекта
    "users.apps.UsersConfig",
    "posts.apps.PostsConfig",
    "media_app.apps.MediaAppConfig",
    "pregnancy.apps.PregnancyConfig",
    "hospitals.apps.HospitalsConfig",
    "chat.apps.ChatConfig",
    "admin_panel.apps.AdminPanelConfig",
    "search_app.apps.SearchAppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "babyblog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "admin_panel.context_processors.site_settings",
            ]
        },
    }
]

WSGI_APPLICATION = "babyblog.wsgi.application"

# ─── База данных ───
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

# ─── Хеширование паролей ───
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── Пользовательская модель ───
AUTH_USER_MODEL = "users.User"

# ─── Локализация ───
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

# ─── Статические файлы ───
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ─── Медиа-файлы ───
MEDIA_URL = "/uploads/"
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", str(BASE_DIR / "uploads"))

# Лимиты загрузки файлов
MAX_IMAGE_SIZE_MB: int = env("MAX_IMAGE_SIZE_MB")
MAX_VIDEO_SIZE_MB: int = env("MAX_VIDEO_SIZE_MB")
MAX_DOCUMENT_SIZE_MB: int = env("MAX_DOCUMENT_SIZE_MB")

# Допустимые типы файлов
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/webm", "video/quicktime"]
ALLOWED_DOCUMENT_TYPES = ["application/pdf", "application/msword"]

# ─── Celery ───
CELERY_BROKER_URL = env("REDIS_URL")
CELERY_RESULT_BACKEND = env("REDIS_URL")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# ─── Email ───
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

# ─── Django REST Framework ───
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# ─── Crispy Forms ───
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ─── Авторизация ───
LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# ─── Первичный ключ ───
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── Логирование ───
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# ─── Безопасность (продакшн) ───
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

# ─── Лимиты загрузки ───
DATA_UPLOAD_MAX_MEMORY_SIZE = 262144000  # 250 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 262144000

# ─── Резервное копирование ───
BACKUP_DIR = os.environ.get("BACKUP_DIR", str(BASE_DIR.parent / "backups"))
