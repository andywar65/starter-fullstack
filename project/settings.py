from pathlib import Path

from django.utils.translation import gettext_lazy as _
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(PROJECT_DIR).resolve().parent
# APPLICATION_DIR = Path(BASE_DIR).resolve(strict=True).parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = ["digitalkomix.com", "www.digitalkomix.com", "localhost", "127.0.0.1"]

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    "grappelli",
    "filebrowser",
    "modeltranslation",
    "tinymce",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.sitemaps",
    # third party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "bootstrap5",
    "django_htmx",
    "debug_toolbar",
    # local
    "users.apps.UsersConfig",
    "pages.apps.PagesConfig",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "project.processors.get_navbar_footer_data",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Database

sqlite_url = "sqlite://" / BASE_DIR / "db.sqlite3"
DATABASES = {"default": env.dj_db_url("DATABASE_URL", default=sqlite_url)}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_QUERY_EMAIL = True

GRAPPELLI_ADMIN_TITLE = env.str("GRAPPELLI_ADMIN_TITLE", default=_("Admin"))

FILEBROWSER_VERSIONS = {
    "admin_thumbnail": {
        "verbose_name": "Admin Thumbnail",
        "width": 60,
        "height": 60,
        "opts": "crop",
    },
    "thumbnail": {
        "verbose_name": "Thumbnail (1 col)",
        "width": 64,
        "height": 64,
        "opts": "crop",
    },
    "small": {"verbose_name": "Small (2 col)", "width": 140, "height": "", "opts": ""},
    "medium": {
        "verbose_name": "Medium (4col )",
        "width": 300,
        "height": "",
        "opts": "",
    },
    "big": {"verbose_name": "Big (6 col)", "width": 460, "height": "", "opts": ""},
    "large": {"verbose_name": "Large (8 col)", "width": 680, "height": "", "opts": ""},
    "wide": {
        "verbose_name": "Landscape 2:1",
        "width": 1600,
        "height": 800,
        "opts": "crop",
    },
    "wide_landscape": {
        "verbose_name": "Landscape 2:1 (legacy)",
        "width": 1600,
        "height": 800,
        "opts": "crop",
    },
    "popup": {"verbose_name": "Popups", "width": 256, "height": 256, "opts": "crop"},
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="en-us")

TIME_ZONE = env.str("TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("it", _("Italian")),
    ("en", _("English")),
]

MODELTRANSLATION_TRANSLATION_FILES = (
    "pages.translation",
    "users.translation",
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]

STATIC_ROOT = env.str("STATIC_ROOT")  # no trailing slash
STATIC_URL = env.str("STATIC_URL", default="/static/")

MEDIA_ROOT = env.str("MEDIA_ROOT")  # no trailing slash
MEDIA_URL = env.str("MEDIA_URL", default="/media/")

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": True,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect | "
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | help",
}

# Mail configuration

EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = env.str("EMAIL_HOST", default="email_host")
EMAIL_PORT = env.int("EMAIL_PORT", default=465)
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="password")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="user")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
SERVER_EMAIL = env.str("SERVER_EMAIL", default="root@localhost")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="webmaster@localhost")
EMAIL_RECIPIENT = env.str("EMAIL_RECIPIENT", default="me@example.com")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

SITE_ID = 1
