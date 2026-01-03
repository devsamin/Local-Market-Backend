import os
from pathlib import Path
from datetime import timedelta
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =======================
# ENV CONFIG
# =======================
env = environ.Env(
    DEBUG=(bool, False)  # default False
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")  # True locally, False in production
ALLOWED_HOSTS = ["*"]

# =======================
# DATABASE CONFIG
# =======================
DEPLOYMENT = env.bool("DEPLOYMENT", default=False)

if DEPLOYMENT:
    DATABASES = {
        "default": dj_database_url.parse(
            env("DATABASE_URL"),
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# =======================
# APPS
# =======================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "django_filters",
    "corsheaders",

    "users",
    "products",
    "orders",
    "reviews",
    "specialOffer",
    "dashboard",
    "payments",
    "cart",
    "category",
]

AUTH_USER_MODEL = "users.User"
ROOT_URLCONF = "localmart_backend.urls"

# =======================
# TEMPLATES
# =======================
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

# =======================
# MIDDLEWARE
# =======================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =======================
# CORS
# =======================
CORS_ALLOW_ALL_ORIGINS = True

# =======================
# DRF
# =======================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# =======================
# STATIC & MEDIA
# =======================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =======================
# STRIPE
# =======================
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")

# =======================
# CUSTOM
# =======================
BACKEND_BASE_URL = env("BACKEND_BASE_URL")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
